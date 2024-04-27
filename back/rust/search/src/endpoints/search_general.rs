use crate::{
    get_context,
    endpoints::{
        common::normalize_recipe,
        EndpointResponse, ErrorResponse, InputPayload, SearchResponse, INTERNAL_SERVER_ERROR,
    },
    context::get_repository,
    repository::{
        models::recipe::Recipe,
        service::{recipe::Repository as RecipeRepository, user::Repository as UserRepository},
    },
};
use salvo::{
    http::StatusCode,
    oapi::extract::JsonBody,
    prelude::{endpoint, Json, Writer},
    Response,
};
use tracing::error;

#[endpoint]
pub async fn search_general(
    payload: JsonBody<InputPayload>,
    res: &mut Response,
) -> Json<EndpointResponse<Recipe>> {
    let context = get_context!(res);
    let payload = payload.into_inner();

    let users = match context.repository.user_collection.find_by_name(&payload.data).await {
        Ok(value) => value,
        Err(e) => {
            error!("Error: {e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            return Json(EndpointResponse::Error(ErrorResponse {
                message: e.to_string(),
            }));
        }
    };

    let recipes = match context.repository.recipe_collection.search(payload).await {
        Ok(mut value) => {
            for recipe in &mut value.data {
                if let Err(e) = normalize_recipe(recipe, &context.repository).await {
                    error!("Error: {e}");
                    res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
                    return Json(EndpointResponse::Error(ErrorResponse {
                        message: INTERNAL_SERVER_ERROR.to_string(),
                    }));
                }
            }
            value
        }
        Err(e) => {
            error!("Error: {e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            return Json(EndpointResponse::Error(ErrorResponse {
                message: e.to_string(),
            }));
        }
    };

    Json(EndpointResponse::SuccessSearch(SearchResponse {
        recipes,
        users,
    }))
}
