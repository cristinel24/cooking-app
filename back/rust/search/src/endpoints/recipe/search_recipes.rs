use crate::{
    context::get_global_context,
    endpoints::{
        common::normalize_recipe, recipe::SearchRecipesPayload, EndpointResponse, ErrorResponse,
        INTERNAL_SERVER_ERROR,
    },
    get_endpoint_context,
    repository::{models::recipe::Recipe, service::recipe::Repository as RecipeRepository},
};
use salvo::{
    http::StatusCode,
    oapi::extract::JsonBody,
    prelude::{endpoint, Json, Writer},
    Response,
};
use tracing::error;

#[endpoint]
pub async fn search_recipes(
    payload: JsonBody<SearchRecipesPayload>,
    res: &mut Response,
) -> Json<EndpointResponse<Recipe>> {
    let context = get_endpoint_context!(res);

    match context
        .repository
        .recipe_collection
        .search(payload.into_inner().to_params())
        .await
    {
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
            Json(EndpointResponse::Success(value))
        }
        Err(e) => {
            error!("Error: {e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            Json(EndpointResponse::Error(ErrorResponse {
                message: e.to_string(),
            }))
        }
    }
}
