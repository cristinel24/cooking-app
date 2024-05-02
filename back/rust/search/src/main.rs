mod context;
mod endpoints;
mod middlewares;
mod repository;
use crate::{
    context::{
        CookingAppContext, EnvironmentVariables, AI_SERVER_VAR, AUTH_SERVER_VAR, CONTEXT,
        MONGO_URI_VAR, PORT, SERVER
    },
    endpoints::{
        recipe::{search_ai_tokens::search_ai_tokens, search_fuzzy_title::search_fuzz_title},
        search_ai::search_ai,
        search_general::search_general,
        user::search_users::search_users,
    },
    middlewares::{auth_handler::auth_handler, error_handler::error_handler},
    repository::cooking_app::CookingAppRepository,
};
use anyhow::Result;
use dotenv::dotenv;
use salvo::{
    conn::TcpListener,
    oapi::{
        security::{Http, HttpAuthScheme},
        SecurityRequirement, SecurityScheme,
    },
    oapi::{OpenApi, RouterExt},
    prelude::SwaggerUi,
    Listener, Router, Server,
};
use tracing::{info, warn};

const DOCS_PATH: &str = "docs";

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt().init();

    let authors = env!("CARGO_PKG_AUTHORS");
    let name = env!("CARGO_PKG_NAME");
    let version = env!("CARGO_PKG_VERSION");

    info!("Package: {}", name);
    info!("Version: {}", version);
    info!("Authors: {}", authors);

    let env_variables = if let Err(e) = dotenv() {
        warn!("Environment file '.env' not found! Full error: {e}");
        EnvironmentVariables::default()
    } else {
        EnvironmentVariables {
            mongo_server: std::env::var(MONGO_URI_VAR)?,
            ai_server: std::env::var(AI_SERVER_VAR)?,
            auth_server: std::env::var(AUTH_SERVER_VAR)?,
            server: std::env::var(SERVER)?,
            port: std::env::var(PORT)?.parse::<u32>()?,
        }
    };
    let (server, port) = (env_variables.server.clone(), env_variables.port);

    CONTEXT
        .set(CookingAppContext {
            repository: CookingAppRepository::new(&env_variables.mongo_server).await?,
            env: env_variables,
        })
        .map_or_else(
            |_| {
                Err(anyhow::Error::msg(
                    "Couldn't initialize CookingApp Repository!",
                ))
            },
            Ok,
        )?;

    let auth_scheme = SecurityScheme::Http(Http::new(HttpAuthScheme::Bearer).bearer_format("JWT"));
    let security_requirement = SecurityRequirement::new("Bearer".to_string(), Vec::<String>::new());

    let raw_router = Router::new().push(
        Router::with_path("/api")
            .hoop(error_handler)
            .push(Router::new().oapi_tag("Search").append(&mut vec![
                        Router::with_path("/search").post(search_general),
                        Router::with_path("/search-ai").hoop(auth_handler)
                            .oapi_security(security_requirement)
                            .post(search_ai)
                    ]))
            .push(Router::new().oapi_tag("Testing").append(&mut vec![
                Router::with_path("/tokens").post(search_ai_tokens),
                Router::with_path("/title/<title>").get(search_fuzz_title),
                Router::with_path("/user/<name>").post(search_users),
            ])),
    );

    let acceptor = TcpListener::new(format!("{server}:{port}")).bind().await;
    let doc = OpenApi::new(name, version)
        .add_security_scheme("Bearer", auth_scheme)
        .merge_router(&raw_router);

    let router = raw_router
        .unshift(doc.into_router(format!("/{DOCS_PATH}.json")))
        .unshift(SwaggerUi::new(format!("/{DOCS_PATH}.json")).into_router(format!("/{DOCS_PATH}")));

    info!("Docs on {server}:{port}/{DOCS_PATH}");
    Server::new(acceptor).serve(router).await;

    Ok(())
}
