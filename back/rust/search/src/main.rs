mod context;
mod endpoints;
mod middlewares;
mod repository;
use crate::{
    context::{CookingAppContext, EnvironmentVariables, CONTEXT},
    endpoints::{
        ai::search_ai::search_ai,
        recipe::search_recipes::search_recipes,
        recipe::{search_ai_tokens::search_ai_tokens, search_fuzzy_title::search_fuzz_title},
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
        security::{ApiKey, ApiKeyValue},
        OpenApi, RouterExt, SecurityRequirement, SecurityScheme,
    },
    prelude::SwaggerUi,
    Listener, Router, Server,
};
use tracing::info;

const DOCS_PATH: &str = "docs";
const X_USER_ID: &str = "X-User-Id";
const X_USER_ROLES: &str = "X-User-Roles";

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt().init();

    let authors = env!("CARGO_PKG_AUTHORS");
    let name = env!("CARGO_PKG_NAME");
    let version = env!("CARGO_PKG_VERSION");

    info!("Package: {}", name);
    info!("Version: {}", version);
    info!("Authors: {}", authors);

    let _ = dotenv();

    let env_variables = EnvironmentVariables::get_env();
    let (host, port) = (env_variables.host.clone(), env_variables.port);

    CONTEXT
        .set(CookingAppContext {
            repository: CookingAppRepository::new(&env_variables.mongo_uri).await?,
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

    let auth_id_scheme = SecurityScheme::ApiKey(ApiKey::Header(ApiKeyValue::new(X_USER_ID)));
    let auth_roles_scheme = SecurityScheme::ApiKey(ApiKey::Header(ApiKeyValue::new(X_USER_ROLES)));
    let security_requirement = SecurityRequirement::new(X_USER_ID, Vec::<String>::new())
        .add(X_USER_ROLES, Vec::<String>::new());

    let raw_router = Router::new()
        .oapi_security(security_requirement)
        .hoop(error_handler)
        .push(Router::new().oapi_tag("Search").append(&mut vec![
            Router::with_path("/users").post(search_users),
            Router::with_path("/recipes").post(search_recipes),
            Router::with_path("/ai").hoop(auth_handler).post(search_ai),
        ]))
        .push(Router::new().oapi_tag("Testing").append(&mut vec![
            Router::with_path("/tokens").post(search_ai_tokens),
            Router::with_path("/title/<title>").get(search_fuzz_title),
            Router::with_path("/user/<name>").post(search_users),
        ]));

    let acceptor = TcpListener::new(format!("{host}:{port}")).bind().await;
    let doc = OpenApi::new(name, version)
        .add_security_scheme(X_USER_ID, auth_id_scheme)
        .add_security_scheme(X_USER_ROLES, auth_roles_scheme)
        .merge_router(&raw_router);

    let router = raw_router
        .unshift(doc.into_router(format!("/{DOCS_PATH}.json")))
        .unshift(SwaggerUi::new(format!("/{DOCS_PATH}.json")).into_router(format!("/{DOCS_PATH}")));

    info!("Docs on {host}:{port}/{DOCS_PATH}");
    Server::new(acceptor).serve(router).await;

    Ok(())
}
