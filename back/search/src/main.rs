mod endpoints;
mod repository;

use crate::endpoints::recipe::search_ai_tokens::search_ai_tokens;
use crate::repository::cooking_app::CookingAppRepository;
use anyhow::Result;
use dotenv::dotenv;
use once_cell::sync::OnceCell;
use salvo::conn::TcpListener;
use salvo::oapi::OpenApi;
use salvo::prelude::SwaggerUi;
use salvo::{handler, Listener, Request, Router, Server};
use tracing::info;
use crate::endpoints::recipe::search_fuzzy_title::search_fuzz_title;

const MONGO_KEY: &str = "MONGO_URI";
const PORT: u32 = 7777u32;
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

    let raw_router = Router::new().push(Router::with_path("/api")
        .hoop(logger_middleware)
        .append(&mut vec![
            Router::with_path("/tokens").post(search_ai_tokens),
            Router::with_path("/title/<title>").get(search_fuzz_title),
    ]));

    let acceptor = TcpListener::new(format!("127.0.0.1:{}", PORT)).bind().await;
    let doc = OpenApi::new("Test", "6.9").merge_router(&raw_router);

    let router = raw_router
        .unshift(doc.into_router("/docs.json"))
        .unshift(SwaggerUi::new("/docs.json").into_router("/docs"));

    info!("Cooking app!");
    info!("Docs on 127.0.0.1:{PORT}/docs");
    Server::new(acceptor).serve(router).await;

    Ok(())
}
