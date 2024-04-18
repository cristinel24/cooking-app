mod endpoints;
mod repository;

use crate::endpoints::test::test_route;
use crate::repository::cooking_app::CookingAppRepository;
use anyhow::Result;
use dotenv::dotenv;
use once_cell::sync::OnceCell;
use salvo::conn::TcpListener;
use salvo::oapi::OpenApi;
use salvo::prelude::SwaggerUi;
use salvo::{Listener, Router, Server};
use tracing::{error, info, trace};

const MONGO_KEY: &str = "MONGO_URI";
pub static CONTEXT: OnceCell<CookingAppRepository> = OnceCell::new();

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
        Router::with_path("/api").append(&mut vec![Router::with_path("/test").post(test_route)]),
    );

    info!("Cooking app!");
    error!("VALELEU");

    let acceptor = TcpListener::new(format!("127.0.0.1:{}", 7777)).bind().await;

    let doc = OpenApi::new("Test", "6.9").merge_router(&raw_router);

    let router = raw_router
        .unshift(doc.into_router("/docs.json"))
        .unshift(SwaggerUi::new("/docs.json").into_router("/docs"));

    info!("Docs on 127.0.0.1:7777/docs");

    Server::new(acceptor).serve(router).await;

    Ok(())
}
