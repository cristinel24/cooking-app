use crate::endpoints::recipe::{
    search_ai_tokens::search_ai_tokens, search_fuzzy_title::search_fuzz_title,
};
use crate::endpoints::{ErrorResponse, INTERNAL_SERVER_ERROR, search_general::search_general, user::search_users::search_users};
use crate::repository::cooking_app::CookingAppRepository;
use anyhow::Result;
use dotenv::dotenv;
use once_cell::sync::OnceCell;
use salvo::{conn::TcpListener, handler, oapi::{OpenApi, RouterExt}, prelude::SwaggerUi, Listener, Request, Router, Server, Response, Depot, FlowCtrl};
use salvo::http::{ResBody, StatusCode};
use salvo::prelude::Json;
use tracing::{info, error};

mod endpoints;
mod repository;

const MONGO_KEY: &str = "MONGO_URI";
const PORT: u32 = 7777u32;
const DOCS_PATH: &str = "docs";

pub static CONTEXT: OnceCell<CookingAppRepository> = OnceCell::new();

#[handler]
async fn error_handler(req: &mut Request, res: &mut Response, depot: &mut Depot, ctrl: &mut FlowCtrl) {
    info!("{} {}", req.method(), req.uri());

    if ctrl.call_next(req, depot, res).await {
        if let ResBody::Error(error) = &res.body {
            let error = ErrorResponse {
                message: error.brief.clone()
            };
            error!("{error:?}");
            res.status_code(StatusCode::BAD_REQUEST);
            res.render(Json(error));
        }
    } else {
        let error = ErrorResponse {
            message: INTERNAL_SERVER_ERROR.to_string()
        };
        error!("{error:?}");
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt().init();
    dotenv()?;

    CONTEXT
        .set(CookingAppRepository::new(std::env::var(MONGO_KEY)?).await?)
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

    let authors = env!("CARGO_PKG_AUTHORS");
    let name = env!("CARGO_PKG_NAME");
    let version = env!("CARGO_PKG_VERSION");

    let acceptor = TcpListener::new(format!("127.0.0.1:{}", PORT)).bind().await;
    let doc = OpenApi::new(name, version).merge_router(&raw_router);

    let router = raw_router
        .unshift(doc.into_router(format!("/{}.json", DOCS_PATH)))
        .unshift(
            SwaggerUi::new(format!("/{}.json", DOCS_PATH)).into_router(format!("/{}", DOCS_PATH)),
        );

    info!("Package: {}", name);
    info!("Version: {}", version);
    info!("Authors: {}", authors);
    info!("Docs on 127.0.0.1:{PORT}/{DOCS_PATH}");
    Server::new(acceptor).serve(router).await;

    Ok(())
}
