mod endpoints;
mod repository;
use crate::endpoints::recipe::{
    search_ai_tokens::search_ai_tokens, search_fuzzy_title::search_fuzz_title,
};
use crate::endpoints::{
    search_general::search_general, user::search_users::search_users, ErrorResponse,
    INTERNAL_SERVER_ERROR,
};
use crate::repository::cooking_app::CookingAppRepository;
use anyhow::Result;
use dotenv::dotenv;
use once_cell::sync::OnceCell;
use salvo::http::{ResBody, StatusCode};
use salvo::prelude::Json;
use salvo::{
    conn::TcpListener,
    handler,
    oapi::{OpenApi, RouterExt},
    prelude::SwaggerUi,
    Depot, FlowCtrl, Listener, Request, Response, Router, Server,
};
use tracing::{error, info};

const MONGO_KEY: &str = "MONGO_URI";
const PORT: u32 = 7777u32;
const DOCS_PATH: &str = "docs";

pub static CONTEXT: OnceCell<CookingAppRepository> = OnceCell::new();
  
#[handler]
async fn error_handler(
    req: &mut Request,
    res: &mut Response,
    depot: &mut Depot,
    ctrl: &mut FlowCtrl,
) {
    info!("{} {}", req.method(), req.uri());

    if ctrl.call_next(req, depot, res).await {
        if let ResBody::Error(error) = &res.body {
            let error = ErrorResponse {
                message: error.brief.clone(),
            };
            error!("{error:?}");
            res.status_code(StatusCode::BAD_REQUEST);
            res.render(Json(error));
        }
    } else {
        let error = ErrorResponse {
            message: INTERNAL_SERVER_ERROR.to_string(),
        };
        error!("{error:?}");
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt().init();

    let authors = env!("CARGO_PKG_AUTHORS");
    let name = env!("CARGO_PKG_NAME");
    let version = env!("CARGO_PKG_VERSION");

    info!("Package: {}", name);
    info!("Version: {}", version);
    info!("Authors: {}", authors);

    if let Err(e) = dotenv() {
        error!("Environment file '.env' not found! Full error: {e}");
    };

    let mongo_uri = std::env::var(MONGO_KEY).unwrap_or("mongodb://localhost:27017".to_owned());

    CONTEXT
        .set(CookingAppRepository::new(mongo_uri).await?)
        .map_or_else(
            |_| {
                Err(anyhow::Error::msg(
                    "Couldn't initialize CookingApp Repository!",
                ))
            },
            Ok,
        )?;

    let raw_router = Router::new().push(
        Router::with_path("/api")
            .hoop(error_handler)
            .push(
                Router::new()
                    .oapi_tag("Search")
                    .append(&mut vec![Router::with_path("/search").post(search_general)]),
            )
            .push(Router::new().oapi_tag("Testing").append(&mut vec![
                Router::with_path("/tokens").post(search_ai_tokens),
                Router::with_path("/title/<title>").get(search_fuzz_title),
                Router::with_path("/user/<name>").post(search_users),
            ])),
    );

    let acceptor = TcpListener::new(format!("127.0.0.1:{}", PORT)).bind().await;
    let doc = OpenApi::new(name, version).merge_router(&raw_router);

    let router = raw_router
        .unshift(doc.into_router(format!("/{}.json", DOCS_PATH)))
        .unshift(
            SwaggerUi::new(format!("/{}.json", DOCS_PATH)).into_router(format!("/{}", DOCS_PATH)),
        );

    info!("Docs on 127.0.0.1:{PORT}/{DOCS_PATH}");
    Server::new(acceptor).serve(router).await;

    Ok(())
}
