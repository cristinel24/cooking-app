use crate::endpoints::recipe::search_fuzzy_title::search_fuzz_title;
use crate::endpoints::search_general::search_general;
use anyhow::Result;
use dotenv::dotenv;
use once_cell::sync::OnceCell;
use salvo::conn::TcpListener;
use salvo::oapi::OpenApi;
use salvo::prelude::SwaggerUi;
use salvo::{handler, Listener, Request, Router, Server};
use tracing::info;

// use crate::endpoints::test::test_route;
use crate::endpoints::recipe::search_ai_tokens::search_ai_tokens;
use crate::endpoints::user::search_users::search_users;
use crate::repository::cooking_app::CookingAppRepository;

mod endpoints;
mod repository;

const MONGO_KEY: &str = "MONGO_URI";
const PORT: u32 = 7777u32;
const DOCS_PATH: &str = "docs";

pub static CONTEXT: OnceCell<CookingAppRepository> = OnceCell::new();

#[handler]
async fn logger_middleware(req: &mut Request) {
    info!("{} {}", req.method(), req.uri());
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

    let raw_router = Router::new().push(Router::with_path("/api").hoop(logger_middleware).append(
        &mut vec![
            Router::with_path("/search").post(search_general),
            Router::with_path("/tokens").post(search_ai_tokens),
            Router::with_path("/title/<title>").get(search_fuzz_title),
            Router::with_path("/user/<name>").post(search_users),
        ],
    ));

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
