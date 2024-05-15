pub mod graceful_shutdown;
pub mod endpoints;

use endpoints::test_doi;

use crate::graceful_shutdown::GracefulShutdown;
use anyhow::{Context, Result};
use common::context::config::get_configuration;
use salvo::{
    handler,
    logging::Logger,
    oapi::{Info, OpenApi},
    prelude::{Router, SwaggerUi, TcpListener},
    Listener, Request, Server,
};
use tracing::info;

#[handler]
async fn test(req: &mut Request) {
    println!("{req:?}")
}

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt()
        .with_ansi(false)
        .with_max_level(tracing_core::Level::TRACE)
        .init();

    let config = get_configuration().context("Invalid configuration file!")?;

    let router = Router::new().push(
        Router::with_path("/api")
            .hoop(Logger::new())
            .hoop(test)
            .append(&mut vec![Router::with_path("/test").get(test_doi)]),
    );

    let doc = OpenApi::new("Cooking APP Gateway", env!("CARGO_PKG_VERSION"))
        .merge_router(&router)
        .info(
            Info::new("Cooking APP Gateway", env!("CARGO_PKG_VERSION"))
                .description("Certified cookers"),
        );

    let router = router
        .unshift(doc.into_router("/docs.json"))
        .unshift(SwaggerUi::new("/docs.json").into_router("/docs"));

    let acceptor = TcpListener::new(format!("{}:{}", config.input.host, config.input.port))
        .bind()
        .await;

    let name = env!("CARGO_PKG_NAME");
    let authors = env!("CARGO_PKG_AUTHORS");

    info!("Started package: {name}!");
    info!("Authors: {}", authors);

    info!(
        "Docs available at: {}:{}/docs",
        config.input.host, config.input.port
    );

    let server = Server::new(acceptor);

    GracefulShutdown::listen(server.handle());
    server.serve(router).await;
    Ok(())
}
