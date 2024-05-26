pub mod config;
pub mod endpoints;
pub mod graceful_shutdown;
mod middlewares;
pub mod models;

use crate::config::{get_configuration, CONTEXT};
use crate::endpoints::ai::{replace_ingredient, talk};
use crate::endpoints::allergen::get_allergen_item;
use crate::endpoints::email_changer::put_email_change;
use crate::endpoints::follow_manager::{
    delete_following_user, get_all_followers, get_all_following, get_followers_count,
    get_user_following_count, put_new_following_user,
};
use crate::endpoints::search_history_manager::{
    delete_item_search_history, get_search_history_endpoint, post_in_search_history,
};
use crate::endpoints::image_storage::{get_image, post_image};
use crate::endpoints::login::request_login_endpoint;
use crate::endpoints::message_history_manager::{delete_history, get_history, put_history};
use crate::endpoints::password_changer::pass_change;
use crate::endpoints::profile_data_changer::patch_profile_data;
use crate::endpoints::rating::{
    delete_rating_endpoint, get_rating_endpoint, patch_rating_endpoint, post_rating_endpoint,
};
use crate::endpoints::recipe_creator::post_recipe_item;
use crate::endpoints::recipe_editor::edit_recipe;
use crate::endpoints::recipe_retriever::{get_card_recipe, get_full_recipe};
use crate::endpoints::recipe_saver::{delete_recipe, put_recipe};
use crate::endpoints::register::request_register_user;
use crate::endpoints::role_changer::change_role;
use crate::endpoints::tag::get_tag_item;
use crate::endpoints::user_destroyer::delete_user;
use crate::endpoints::user_retriever::{
    get_user_card_item, get_user_data_item, get_user_profile_item, post_user_card_item,
};
use crate::endpoints::username_changer::change_username;
use crate::endpoints::verifier::verify;
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
use crate::endpoints::search::{ai_endpoint, recipes_endpoint, users_endpoint};

#[endpoint]
async fn test() {}

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt()
        .with_max_level(tracing_core::Level::TRACE)
        .init();

    let config = get_configuration().context("Invalid configuration file!")?;
    let auth_scheme = SecurityScheme::ApiKey(ApiKey::Header(ApiKeyValue::new(AUTH_HEADER)));
    let security_requirement = SecurityRequirement::new(AUTH_HEADER, Vec::<String>::new());

    let router = Router::new().hoop(Logger::new()).push(
        Router::with_path("/api")
            .hoop(auth_middleware)
            .oapi_security(security_requirement.clone())
            .append(&mut vec![
                setup_rating_routes(),
                setup_tag_routes(),
                setup_allergen_routes(),
                setup_user_saved_recipes_routes(),
                setup_user_routes(),
                setup_profile_routes(),
                setup_misc_routes(),
                setup_search_routes(),
                setup_email_changer(),
                setup_ai_routes(),
                setup_password_changer(),
                setup_login(),
                setup_register(),
            ]),
    );

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

fn setup_search_routes() -> Router {
    Router::with_path("/search")
        .oapi_tag("SEARCH")
        .append(&mut vec![
            Router::with_path("/ai")
                .post(ai_endpoint),
            Router::with_path("/recipes")
                .post(recipes_endpoint),
            Router::with_path("/users")
                .post(users_endpoint),
        ])
}

fn setup_email_changer() -> Router {
    Router::with_path("/user/email")
        .oapi_tag("EMAIL CHANGER")
        .put(put_email_change)
}

fn setup_password_changer() -> Router {
    Router::with_path("/user/password")
        .oapi_tag("PASSWORD CHANGER")
        .put(pass_change)
}

fn setup_login() -> Router {
    Router::with_path("/login")
        .oapi_tag("LOGIN")
        .post(request_login_endpoint)
}

fn setup_register() -> Router {
    Router::with_path("/register")
        .oapi_tag("REGISTER")
        .put(request_register_user)
}

fn setup_ai_routes() -> Router {
    Router::with_path("/ai").oapi_tag("AI").append(&mut vec![
        Router::with_path("/tokenize/replace_ingredient").post(replace_ingredient),
        Router::with_path("/chatbot").post(talk),
    ])
}

fn setup_rating_routes() -> Router {
    Router::with_path("/rating")
        .oapi_tag("RATING")
        .append(&mut vec![
            Router::with_path("/<parent_id>/replies")
                .get(get_rating_endpoint)
                .post(post_rating_endpoint),
            Router::with_path("/<rating_id>")
                .patch(patch_rating_endpoint)
                .delete(delete_rating_endpoint),
        ])
}

fn setup_tag_routes() -> Router {
    Router::with_path("/tag").oapi_tag("TAG").get(get_tag_item)
}

fn setup_allergen_routes() -> Router {
    Router::with_path("/allergen")
        .oapi_tag("ALLERGEN")
        .get(get_allergen_item)
}

fn setup_user_saved_recipes_routes() -> Router {
    Router::with_path("/user/<user_id>/saved-recipes/<recipe_id>")
        .oapi_tag("RECIPE SAVER")
        .put(put_recipe)
        .delete(delete_recipe)
}

fn setup_user_routes() -> Router {
    Router::with_path("/user")
        .append(&mut vec![
            Router::with_path("/<user_id>")
                .oapi_tag("USER RETRIEVER")
                .get(get_user_data_item)
                .append(&mut vec![
                    Router::with_path("/card").get(get_user_card_item),
                    Router::with_path("/profile").get(get_user_profile_item),
                ]),
            Router::new()
                .oapi_tag("USER RETRIEVER")
                .post(post_user_card_item),
        ])
        .push(
            Router::with_path("/<user_id>/search-history")
                .oapi_tag("SEARCH HISTORY")
                .get(get_search_history_endpoint)
                .post(post_in_search_history)
                .delete(delete_item_search_history),
        )
        .push(
            Router::with_path("/<user_id>")
                .oapi_tag("FOLLOW MANAGER")
                .append(&mut vec![
                    Router::with_path("/followers")
                        .get(get_all_followers)
                        .push(Router::with_path("/count").get(get_followers_count)),
                    Router::with_path("/following")
                        .push(Router::with_path("/count").get(get_user_following_count))
                        .get(get_all_following)
                        .put(put_new_following_user)
                        .delete(delete_following_user),
                ]),
        )
        .push(
            Router::with_path("/<user_id>/message-history")
                .oapi_tag("MESSAGE HISTORY")
                .get(get_history)
                .post(put_history)
                .delete(delete_history),
        )
        .push(
            Router::with_path("/<user_id>")
                .oapi_tag("USER DESTROYER")
                .delete(delete_user),
        )
        .push(
            Router::with_path("/<user_id>/roles")
                .oapi_tag("ROLE CHANGER")
                .put(change_role),
        )
        .push(
            Router::with_path("/username")
                .oapi_tag("USERNAME CHANGER")
                .put(change_username),
        )
}

fn setup_profile_routes() -> Router {
    Router::with_path("/profile")
        .oapi_tag("PROFILE DATA CHANGER")
        .push(Router::with_path("/<user_id>").patch(patch_profile_data))
}

fn setup_misc_routes() -> Router {
    Router::new().append(&mut vec![
        Router::with_path("/images")
            .oapi_tag("IMAGE STORAGE")
            .put(post_image)
            .push(Router::with_path("/<image_id>").get(get_image)),
        Router::with_path("/recipe")
            .oapi_tag("RECIPE CREATOR")
            .post(post_recipe_item),
        Router::with_path("/recipe/<recipe_id>")
            .oapi_tag("RECIPE RETRIEVER")
            .get(get_full_recipe)
            .push(Router::with_path("/card").get(get_card_recipe)),
        Router::with_path("/recipe/<recipe_id>")
            .oapi_tag("RECIPE EDITOR")
            .patch(edit_recipe),
        Router::with_path("/verify")
            .oapi_tag("VERIFIER")
            .patch(verify),
    ])
}
