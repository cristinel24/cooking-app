pub mod config;
pub mod endpoints;
pub mod graceful_shutdown;
mod middlewares;
pub mod models;

use crate::config::{get_configuration, CONTEXT};
use crate::endpoints::ai::{chatbot_route, replace_ingredient_route};
use crate::endpoints::allergen_manager::get_allergens_route;
use crate::endpoints::email_changer::email_change;
use crate::endpoints::follow_manager::{
    delete_following_user, get_all_followers, get_all_following, get_followers_count,
    get_user_following_count, post_new_following_user,
};
use crate::endpoints::image_storage::{get_image, post_image};
use crate::endpoints::login::request_login_endpoint;
use crate::endpoints::message_history_manager::{delete_history, get_history, post_history};
use crate::endpoints::password_changer::pass_change;
use crate::endpoints::profile_data_changer::patch_profile_data;
use crate::endpoints::rating_manager::{
    delete_rating_endpoint, get_rating_comments_endpoint, patch_rating_endpoint,
    post_rating_endpoint,
};
use crate::endpoints::recipe_creator::post_recipe_item;
use crate::endpoints::recipe_editor::edit_recipe;
use crate::endpoints::recipe_retriever::{get_card_recipe, get_full_recipe};
use crate::endpoints::recipe_saver::{delete_recipe, put_recipe};
use crate::endpoints::register::request_register_user;
use crate::endpoints::role_changer::change_role;
use crate::endpoints::search::{ai_endpoint, recipes_endpoint, users_endpoint};
use crate::endpoints::search_history_manager::{
    delete_item_search_history, get_search_history_endpoint, post_in_search_history,
};
use crate::endpoints::tag_manager::get_tags;
use crate::endpoints::user_destroyer::delete_user;
use crate::endpoints::user_retriever::{
    get_user_card_item, get_user_data_item, get_user_profile_item, post_user_card_item,
};
use crate::endpoints::username_changer::username_change;
use crate::endpoints::verifier::verify;
use crate::graceful_shutdown::GracefulShutdown;
use crate::middlewares::auth::{auth_middleware, AUTH_HEADER};
use anyhow::{Context, Result};
use endpoints::credentials_change_requester::request_credentials_change;
use endpoints::rating_manager::{
    delete_recipe_ratings_endpoint, get_rating_by_id_endpoint,
    get_rating_by_recipe_and_author_endpoint, get_recipe_comments_endpoint,
};
use endpoints::recipe_saver::get_saved_recipes;
use salvo::cors::{AllowMethods, AllowOrigin, Cors};
use salvo::http::HeaderName;
use salvo::oapi::security::{ApiKey, ApiKeyValue};
use salvo::oapi::{endpoint, SecurityRequirement, SecurityScheme};
use salvo::Service;
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
        .with_max_level(tracing_core::Level::INFO)
        .init();

    let cors = Cors::new()
        .allow_origin(AllowOrigin::any())
        .allow_methods(AllowMethods::any())
        // .allow_headers(AllowHeaders::any())
        .allow_headers(vec![
            HeaderName::from_lowercase(b"authorization")?,
            HeaderName::from_lowercase(b"*")?,
        ])
        .into_handler();

    let config = get_configuration().context("Invalid configuration file!")?;
    let auth_scheme = SecurityScheme::ApiKey(ApiKey::Header(ApiKeyValue::new(AUTH_HEADER)));
    let security_requirement = SecurityRequirement::new(AUTH_HEADER, Vec::<String>::new());

    let router = Router::new().hoop(Logger::new()).push(
        Router::with_path("/api")
            .hoop(auth_middleware)
            .oapi_security(security_requirement.clone())
            .append(&mut vec![
                ai_router(),
                allergen_manager_router(),
                credentials_change_requester_router(),
                email_changer_router(),
                follow_manager_router(),
                image_storage_router(),
                login_router(),
                message_history_manager_router(),
                password_changer_router(),
                profile_data_changer_router(),
                rating_manager_router(),
                recipe_creator_router(),
                recipe_editor_router(),
                recipe_retriever_router(),
                recipe_saver_router(),
                register_router(),
                role_changer_router(),
                search_router(),
                search_history_manager_router(),
                tag_manager_router(),
                user_destroyer_router(),
                user_retriever_router(),
                username_changer_router(),
                verifier_router(),
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
    let service = Service::new(router).hoop(cors);
    server.serve(service).await;
    Ok(())
}

fn ai_router() -> Router {
    Router::with_path("/ai").oapi_tag("AI").append(&mut vec![
        Router::with_path("/tokenize/replace_ingredient").post(replace_ingredient_route),
        Router::with_path("/chatbot").post(chatbot_route),
    ])
}

fn allergen_manager_router() -> Router {
    Router::with_path("/allergens")
        .oapi_tag("ALLERGEN MANAGER")
        .get(get_allergens_route)
}

fn credentials_change_requester_router() -> Router {
    Router::with_path("/auth/change-credentials")
        .oapi_tag("CREDENTIALS CHANGE REQUESTER")
        .post(request_credentials_change)
}

fn email_changer_router() -> Router {
    Router::with_path("/auth/change-email")
        .oapi_tag("EMAIL CHANGER")
        .post(email_change)
}

fn follow_manager_router() -> Router {
    Router::with_path("/users/<user_id>")
        .oapi_tag("FOLLOW MANAGER")
        .append(&mut vec![
            Router::with_path("/followers")
                .get(get_all_followers)
                .push(Router::with_path("/count").get(get_followers_count)),
            Router::with_path("/following")
                .get(get_all_following)
                .push(Router::with_path("/count").get(get_user_following_count)),
            Router::with_path("/follow")
                .post(post_new_following_user)
                .delete(delete_following_user),
        ])
}

fn image_storage_router() -> Router {
    Router::with_path("/images")
        .oapi_tag("IMAGE STORAGE")
        .post(post_image)
        .push(Router::with_path("/<image_id>").get(get_image))
}

fn login_router() -> Router {
    Router::with_path("/auth/login")
        .oapi_tag("LOGIN")
        .post(request_login_endpoint)
}

fn message_history_manager_router() -> Router {
    Router::with_path("/users/<user_id>/message-history")
        .oapi_tag("MESSAGE HISTORY")
        .get(get_history)
        .post(post_history)
        .delete(delete_history)
}

fn password_changer_router() -> Router {
    Router::with_path("/auth/change-password")
        .oapi_tag("PASSWORD CHANGER")
        .post(pass_change)
}

fn profile_data_changer_router() -> Router {
    Router::with_path("/users/<user_id>")
        .oapi_tag("PROFILE DATA CHANGER")
        .patch(patch_profile_data)
}

fn rating_manager_router() -> Router {
    Router::new().oapi_tag("RATING MANAGER").append(&mut vec![
        Router::with_path("/ratings")
            .get(get_rating_by_recipe_and_author_endpoint)
            .post(post_rating_endpoint)
            .push(
                Router::with_path("/<parent_id>")
                    .get(get_rating_by_id_endpoint)
                    .push(Router::with_path("/comments").get(get_rating_comments_endpoint))
                    .patch(patch_rating_endpoint)
                    .delete(delete_rating_endpoint),
            ),
        Router::with_path("/recipes/<parent_id>").append(&mut vec![
            Router::with_path("/comments").get(get_recipe_comments_endpoint),
            Router::with_path("/ratings").delete(delete_recipe_ratings_endpoint),
        ]),
    ])
}

fn recipe_creator_router() -> Router {
    Router::with_path("/recipes")
        .oapi_tag("RECIPE CREATOR")
        .post(post_recipe_item)
}

fn recipe_editor_router() -> Router {
    Router::with_path("/recipes/<recipe_id>")
        .oapi_tag("RECIPE EDITOR")
        .patch(edit_recipe)
}

fn recipe_retriever_router() -> Router {
    Router::with_path("/recipes/<recipe_id>")
        .oapi_tag("RECIPE RETRIEVER")
        .get(get_full_recipe)
        .push(Router::with_path("/card").get(get_card_recipe))
}

fn recipe_saver_router() -> Router {
    Router::with_path("/users/<user_id>/saved-recipes")
        .oapi_tag("RECIPE SAVER")
        .get(get_saved_recipes)
        .push(
            Router::with_path("/<recipe_id>")
                .put(put_recipe)
                .delete(delete_recipe),
        )
}

fn register_router() -> Router {
    Router::with_path("/auth/register")
        .oapi_tag("REGISTER")
        .post(request_register_user)
}

fn role_changer_router() -> Router {
    Router::with_path("/users/<user_id>/roles")
        .oapi_tag("ROLE CHANGER")
        .put(change_role)
}

fn search_router() -> Router {
    Router::with_path("/search")
        .oapi_tag("SEARCH")
        .append(&mut vec![
            Router::with_path("/ai").post(ai_endpoint),
            Router::with_path("/recipes").post(recipes_endpoint),
            Router::with_path("/users").post(users_endpoint),
        ])
}

fn search_history_manager_router() -> Router {
    Router::with_path("/users/<user_id>/search-history")
        .oapi_tag("SEARCH HISTORY")
        .get(get_search_history_endpoint)
        .post(post_in_search_history)
        .delete(delete_item_search_history)
}

fn tag_manager_router() -> Router {
    Router::with_path("/tags").oapi_tag("TAG MANAGER").get(get_tags)
}

fn user_destroyer_router() -> Router {
    Router::with_path("/users/<user_id>")
        .oapi_tag("USER DESTROYER")
        .delete(delete_user)
}

fn user_retriever_router() -> Router {
    Router::with_path("/users")
        .oapi_tag("USER RETRIEVER")
        .post(post_user_card_item)
        .push(
            Router::with_path("/<user_id>")
                .get(get_user_data_item)
                .append(&mut vec![
                    Router::with_path("/card").get(get_user_card_item),
                    Router::with_path("/profile").get(get_user_profile_item),
                ]),
        )
}

fn username_changer_router() -> Router {
    Router::with_path("/auth/change-username")
        .oapi_tag("USERNAME CHANGER")
        .post(username_change)
}

fn verifier_router() -> Router {
    Router::with_path("/auth/verify")
        .oapi_tag("VERIFIER")
        .post(verify)
}
