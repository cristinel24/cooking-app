pub mod config;
pub mod endpoints;
pub mod graceful_shutdown;
pub mod models;
pub mod service;

use crate::config::{get_configuration, CONTEXT};
use crate::endpoints::allergen::{delete_allergen_item, get_allergen_item, post_allergen_item};
use crate::endpoints::recipe_saver::{delete_recipe, put_recipe};
use crate::endpoints::tag::{delete_tag_item, get_tag_item, post_tag_item};
use crate::endpoints::{
    hash::{get_hash_primary, get_hash_with},
    rating::{
        delete_rating_endpoint, get_rating_endpoint, patch_rating_endpoint, put_rating_endpoint,
    },
};
use crate::graceful_shutdown::GracefulShutdown;
use anyhow::{Context, Result};
use salvo::oapi::security::{ApiKey, ApiKeyValue};
use salvo::oapi::{endpoint, SecurityRequirement, SecurityScheme};
use salvo::{
    handler,
    logging::Logger,
    oapi::{Info, OpenApi},
    prelude::{Router, RouterExt, SwaggerUi, TcpListener},
    Depot, FlowCtrl, Listener, Request, Response, Server,
};
use tracing::info;
use crate::endpoints::user_retriever::{get_user_card_item, get_user_data_item, get_user_profile_item, post_user_card_item};

pub const HEADER_KEYS: [&str; 2] = ["X-User-Id", "X-User-Roles"];

#[handler]
async fn auth_middleware(
    req: &mut Request,
    depot: &mut Depot,
    res: &mut Response,
    ctrl: &mut FlowCtrl,
) {
    let headers = req.headers_mut();
    let _authorization = headers.get::<String>(AUTH_HEADER.to_string());
    headers.remove("Content-length");
    // let headers = HEADER_KEYS.iter()
    //     .map(|header| (header, None)) // TODO: call some serice to get user_id/roles
    //     .collect::<Vec<_>>();
    ctrl.call_next(req, depot, res).await;
}

#[endpoint]
async fn test() {}

const AUTH_HEADER: &str = "Authorization";

#[allow(clippy::too_many_lines)]
#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt()
        .with_ansi(false)
        .with_max_level(tracing_core::Level::TRACE)
        .init();

    let config = get_configuration().context("Invalid configuration file!")?;
    let auth_scheme = SecurityScheme::ApiKey(ApiKey::Header(ApiKeyValue::new(AUTH_HEADER)));
    let security_requirement = SecurityRequirement::new(AUTH_HEADER, Vec::<String>::new());

    let router = Router::new().hoop(Logger::new()).append(&mut vec![
        Router::with_path("/rating")
            .oapi_tag("RATING")
            .append(&mut vec![
                Router::with_path("/<parent_id>/replies").get(get_rating_endpoint),
                Router::with_path("/<parent_id>/replies")
                    .hoop(auth_middleware)
                    .oapi_security(security_requirement.clone())
                    .put(put_rating_endpoint),
                Router::with_path("/<rating_id>")
                    .hoop(auth_middleware)
                    .oapi_security(security_requirement.clone())
                    .patch(patch_rating_endpoint)
                    .delete(delete_rating_endpoint),
            ]),
        Router::with_path("/hash")
            .oapi_tag("HASH")
            .append(&mut vec![
                Router::with_path("/<target>").get(get_hash_primary),
                Router::with_path("/<hash_algorithm_name>/<target>").get(get_hash_with),
            ]),
        Router::with_path("/tag")
            .oapi_tag("TAG")
            .get(get_tag_item)
            .push(
                Router::with_path("/<name>")
                    .post(post_tag_item)
                    .delete(delete_tag_item),
            ),
        Router::with_path("/allergen")
            .oapi_tag("ALLERGEN")
            .get(get_allergen_item)
            .push(
                Router::with_path("/<name>")
                    .post(post_allergen_item)
                    .delete(delete_allergen_item),
            ),
        Router::with_path("/user/<user_id>/saved-recipes")
            .oapi_tag("RECIPE SAVER")
            .hoop(auth_middleware)
            .oapi_security(security_requirement.clone())
            .put(put_recipe)
            .delete(delete_recipe),
        Router::with_path("/user")
            .oapi_tag("USER RETRIEVER")
            .append(&mut vec![
                Router::with_path("/<user_id>").get(get_user_data_item).append(&mut vec![
                    Router::with_path("/card").get(get_user_card_item),
                    Router::with_path("/profile")
                        .hoop(auth_middleware)
                        .oapi_security(security_requirement.clone())
                        .get(get_user_profile_item),
                ]),
                Router::with_path("/user-cards").post(post_user_card_item),
            ]),
        Router::with_path("/email")
            .oapi_tag("EMAIL")
            .append(&mut vec![
                Router::with_path("/verify-account").post(test),
                Router::with_path("/request-change").post(test),
            ]),
        Router::with_path("/user").oapi_tag("ROLE CHANGER").push(
            Router::with_path("/<user_id>/roles")
                .hoop(auth_middleware)
                .oapi_security(security_requirement.clone()),
        ),
        Router::with_path("/user/<user_id>")
            .oapi_tag("SEARCH HISTORY")
            .push(
                Router::with_path("/search-history")
                    .hoop(auth_middleware)
                    .oapi_security(security_requirement.clone())
                    .get(test)
                    .put(test)
                    .delete(test),
            ),
        Router::with_path("/user/<user_id>")
            .oapi_tag("FOLLOW MANAGER")
            .append(&mut vec![
                Router::with_path("/followers")
                    .push(Router::with_path("/count").get(test))
                    .get(test),
                Router::with_path("/following")
                    .push(Router::with_path("/count").get(test))
                    .get(test),
                Router::with_path("/following")
                    .hoop(auth_middleware)
                    .oapi_security(security_requirement.clone())
                    .put(test)
                    .delete(test),
            ]),
        Router::with_path("/user/<user_id>")
            .oapi_tag("MESSAGE HISTORY")
            .hoop(auth_middleware)
            .oapi_security(security_requirement.clone())
            .push(
                Router::with_path("/message-history")
                    .get(test)
                    .put(test)
                    .delete(test),
            ),
        Router::with_path("/user/<user_id>")
            .oapi_tag("USER DESTROYER")
            .hoop(auth_middleware)
            .oapi_security(security_requirement.clone())
            .delete(test),
        Router::with_path("/profile")
            .oapi_tag("PROFILE DATA CHANGER")
            .hoop(auth_middleware)
            .oapi_security(security_requirement.clone())
            .push(Router::with_path("/<user_id>").patch(test)),
        Router::with_path("/token")
            .oapi_tag("TOKEN VALIDATOR")
            .append(&mut vec![
                Router::with_path("/<type>/<token>").get(test),
                Router::with_path("/<token>").get(test),
            ]),
        Router::with_path("/id").oapi_tag("ID GENERATOR").get(test),
        Router::with_path("/token")
            .oapi_tag("TOKEN GENERATOR")
            .push(Router::with_path("/<user_id>/<type>").get(test)),
        Router::with_path("/image")
            .oapi_tag("IMAGE STORAGE")
            .put(test)
            .push(Router::with_path("/<image_id>").get(test)),
        Router::with_path("/register")
            .oapi_tag("REGISTER")
            .hoop(auth_middleware)
            .oapi_security(security_requirement.clone())
            .post(test),
        Router::with_path("/token")
            .oapi_tag("TOKEN DESTROYER")
            .hoop(auth_middleware)
            .oapi_security(security_requirement.clone())
            .append(&mut vec![
                Router::with_path("/<user_id>/all").delete(test),
                Router::with_path("/<token>").delete(test),
            ]),
        Router::with_path("/verify").oapi_tag("VERIFIER").post(test),
        Router::with_path("/login").oapi_tag("LOGIN").post(test),
        Router::with_path("/creds")
            .oapi_tag("CREDENTIALS CHANGE REQUESTER")
            .hoop(auth_middleware)
            .oapi_security(security_requirement.clone())
            .post(test),
        Router::with_path("/username")
            .oapi_tag("USERNAME CHANGER")
            .hoop(auth_middleware)
            .oapi_security(security_requirement.clone())
            .post(test),
        Router::with_path("/password")
            .oapi_tag("PASSWORD CHANGER")
            .hoop(auth_middleware)
            .oapi_security(security_requirement.clone())
            .post(test),
        Router::with_path("/email")
            .oapi_tag("EMAIL CHANGER")
            .hoop(auth_middleware)
            .oapi_security(security_requirement.clone())
            .post(test),
        Router::with_path("/recipe")
            .oapi_tag("RECIPE CREATOR")
            .hoop(auth_middleware)
            .oapi_security(security_requirement.clone())
            .post(test),
        Router::with_path("/recipe/<recipe_id>")
            .oapi_tag("RECIPE EDITOR")
            .hoop(auth_middleware)
            .oapi_security(security_requirement.clone())
            .post(test),
        Router::with_path("/recipe/<recipe_id>")
            .oapi_tag("RECIPE DESTROYER")
            .hoop(auth_middleware)
            .oapi_security(security_requirement.clone())
            .delete(test),
        Router::with_path("/recipe/<recipe_id>")
            .oapi_tag("RECIPE RATING MANAGER")
            .hoop(auth_middleware)
            .oapi_security(security_requirement.clone())
            .push(
                Router::with_path("/ratings")
                    .put(test)
                    .push(Router::with_path("/<rating_id>").patch(test).delete(test)),
            ),
        Router::with_path("/recipe/<recipe_id>")
            .oapi_tag("RECIPE RETRIEVER")
            .get(test)
            .push(Router::with_path("/card").get(test)),
    ]);

    println!("{router:#?}");

    let doc = OpenApi::new("Cooking APP Gateway", env!("CARGO_PKG_VERSION"))
        .add_security_scheme(AUTH_HEADER, auth_scheme)
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

    CONTEXT.set(config).map_or_else(
        |_| {
            Err(anyhow::Error::msg(
                "Couldn't initialize CookingApp Configuration!",
            ))
        },
        Ok,
    )?;

    let server = Server::new(acceptor);

    GracefulShutdown::listen(server.handle());
    server.serve(router).await;
    Ok(())
}
