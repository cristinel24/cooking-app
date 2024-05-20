pub mod config;
pub mod endpoints;
pub mod graceful_shutdown;
mod middlewares;
pub mod models;

use crate::config::{get_configuration, CONTEXT};
use crate::endpoints::allergen::{delete_allergen_item, get_allergen_item, post_allergen_item};
use crate::endpoints::email::{request_change, verify_account};
use crate::endpoints::history_manager::{
    delete_item_search_history, get_search_history_endpoint, put_in_search_history,
};
use crate::endpoints::recipe_saver::{delete_recipe, put_recipe};
use crate::endpoints::role_changer::admin_role_changer_endpoint;
use crate::endpoints::tag::{delete_tag_item, get_tag_item, post_tag_item};
use crate::endpoints::user_retriever::{
    get_user_card_item, get_user_data_item, get_user_profile_item, post_user_card_item,
};
use crate::endpoints::{
    hash::{get_hash_primary, get_hash_with},
    rating::{
        delete_rating_endpoint, get_rating_endpoint, patch_rating_endpoint, put_rating_endpoint,
    },
};
use crate::graceful_shutdown::GracefulShutdown;
use crate::middlewares::auth::{auth_middleware, AUTH_HEADER};
use anyhow::{Context, Result};
use salvo::oapi::security::{ApiKey, ApiKeyValue};
use salvo::oapi::{endpoint, SecurityRequirement, SecurityScheme};
use salvo::{
    logging::Logger,
    oapi::{Info, OpenApi},
    prelude::{Router, RouterExt, SwaggerUi, TcpListener},
    Listener, Server,
};
use tracing::info;

#[endpoint]
async fn test() {}

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
        setup_rating_routes(auth_middleware, &security_requirement),
        setup_hash_routes(),
        setup_tag_routes(),
        setup_allergen_routes(),
        setup_user_saved_recipes_routes(auth_middleware, &security_requirement),
        setup_user_routes(auth_middleware, &security_requirement),
        setup_profile_routes(auth_middleware, &security_requirement),
        setup_token_routes(auth_middleware, &security_requirement),
        setup_misc_routes(auth_middleware, &security_requirement),
        setup_email_routes(),
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

fn setup_rating_routes(
    auth_middleware: auth_middleware,
    security_requirement: &SecurityRequirement,
) -> Router {
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
        ])
}

fn setup_hash_routes() -> Router {
    Router::with_path("/hash")
        .oapi_tag("HASH")
        .append(&mut vec![
            Router::with_path("/<target>").get(get_hash_primary),
            Router::with_path("/<hash_algorithm_name>/<target>").get(get_hash_with),
        ])
}

fn setup_tag_routes() -> Router {
    Router::with_path("/tag")
        .oapi_tag("TAG")
        .get(get_tag_item)
        .push(
            Router::with_path("/<name>")
                .post(post_tag_item)
                .delete(delete_tag_item),
        )
}

fn setup_allergen_routes() -> Router {
    Router::with_path("/allergen")
        .oapi_tag("ALLERGEN")
        .get(get_allergen_item)
        .push(
            Router::with_path("/<name>")
                .post(post_allergen_item)
                .delete(delete_allergen_item),
        )
}

fn setup_user_saved_recipes_routes(
    auth_middleware: auth_middleware,
    security_requirement: &SecurityRequirement,
) -> Router {
    Router::with_path("/user/<user_id>/saved-recipes")
        .oapi_tag("RECIPE SAVER")
        .hoop(auth_middleware)
        .oapi_security(security_requirement.clone())
        .put(put_recipe)
        .delete(delete_recipe)
}

fn setup_user_routes(
    auth_middleware: auth_middleware,
    security_requirement: &SecurityRequirement,
) -> Router {
    Router::with_path("/user")
        .append(&mut vec![
            Router::with_path("/<user_id>")
                .oapi_tag("USER RETRIEVER")
                .get(get_user_data_item)
                .append(&mut vec![
                    Router::with_path("/card").get(get_user_card_item),
                    Router::with_path("/profile")
                        .hoop(auth_middleware)
                        .oapi_security(security_requirement.clone())
                        .get(get_user_profile_item),
                ]),
            Router::with_path("/user-cards").post(post_user_card_item),
        ])
        .push(
            Router::with_path("/<user_id>/roles")
                .oapi_tag("ROLE CHANGER")
                .hoop(auth_middleware)
                .oapi_security(security_requirement.clone())
                .patch(admin_role_changer_endpoint),
        )
        .push(
            Router::with_path("/<user_id>/search-history")
                .oapi_tag("SEARCH HISTORY")
                .hoop(auth_middleware)
                .oapi_security(security_requirement.clone())
                .get(get_search_history_endpoint)
                .put(put_in_search_history)
                .delete(delete_item_search_history),
        )
        .push(
            Router::with_path("/<user_id>/followers")
                .oapi_tag("FOLLOW MANAGER")
                .push(Router::with_path("/count").get(test))
                .get(test)
                .push(
                    Router::with_path("/following")
                        .push(Router::with_path("/count").get(test))
                        .get(test)
                        .hoop(auth_middleware)
                        .oapi_security(security_requirement.clone())
                        .put(test)
                        .delete(test),
                ),
        )
        .push(
            Router::with_path("/<user_id>/message-history")
                .oapi_tag("MESSAGE HISTORY")
                .hoop(auth_middleware)
                .oapi_security(security_requirement.clone())
                .push(
                    Router::with_path("/message-history")
                        .get(test)
                        .put(test)
                        .delete(test),
                ),
        )
        .push(
            Router::with_path("/<user_id>")
                .oapi_tag("USER DESTROYER")
                .hoop(auth_middleware)
                .oapi_security(security_requirement.clone())
                .delete(test),
        )
}

fn setup_profile_routes(
    auth_middleware: auth_middleware,
    security_requirement: &SecurityRequirement,
) -> Router {
    Router::with_path("/profile")
        .oapi_tag("PROFILE DATA CHANGER")
        .hoop(auth_middleware)
        .oapi_security(security_requirement.clone())
        .push(Router::with_path("/<user_id>").patch(test))
}

fn setup_token_routes(
    auth_middleware: auth_middleware,
    security_requirement: &SecurityRequirement,
) -> Router {
    Router::with_path("/token")
        .oapi_tag("TOKEN VALIDATOR")
        .append(&mut vec![
            Router::with_path("/<type>/<token>").get(test),
            Router::with_path("/<token>").get(test),
        ])
        .push(Router::with_path("/<user_id>/<type>").get(test))
        .push(
            Router::with_path("/<user_id>/all")
                .oapi_tag("TOKEN DESTROYER")
                .hoop(auth_middleware)
                .oapi_security(security_requirement.clone())
                .delete(test),
        )
        .push(
            Router::with_path("/<token>")
                .hoop(auth_middleware)
                .oapi_security(security_requirement.clone())
                .delete(test),
        )
}

fn setup_misc_routes(
    auth_middleware: auth_middleware,
    security_requirement: &SecurityRequirement,
) -> Router {
    Router::new().append(&mut vec![
        Router::with_path("/id").oapi_tag("ID GENERATOR").get(test),
        Router::with_path("/image")
            .oapi_tag("IMAGE STORAGE")
            .put(test)
            .push(Router::with_path("/<image_id>").get(test)),
        Router::with_path("/register")
            .oapi_tag("REGISTER")
            .hoop(auth_middleware)
            .oapi_security(security_requirement.clone())
            .post(test),
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
    ])
}

fn setup_email_routes() -> Router {
    Router::with_path("/email")
        .oapi_tag("EMAIL")
        .append(&mut vec![
            Router::with_path("/verify-account").post(verify_account),
            Router::with_path("/request-change").post(request_change),
        ])
}
