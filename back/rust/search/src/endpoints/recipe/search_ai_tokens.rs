use crate::{
    get_endpoint_context,
    context::get_global_context,
    endpoints::{
        recipe::AiTokensPayload,
        AggregationResponse, EndpointResponse, ErrorResponse, INTERNAL_SERVER_ERROR,
    },
    repository::{
        models::recipe::Recipe,
        service::recipe::Repository as RecipeRepository
    },
};
use salvo::{
    http::StatusCode,
    oapi::extract::JsonBody,
    prelude::{endpoint, Json, Writer},
    Response,
};
use tracing::error;
use crate::endpoints::common::normalize_recipe;

#[endpoint(
    responses(
        (
            status_code = StatusCode::OK,
            body = AggregationResponse<Recipe>,
            example = json!(AggregationResponse::<Recipe>::default())
        ),
        (
            status_code = StatusCode::INTERNAL_SERVER_ERROR,
            body = ErrorResponse,
            example = json!(ErrorResponse::default())
        )
    )
)]
pub async fn search_ai_tokens(
    ai_tokens: JsonBody<AiTokensPayload>,
    res: &mut Response,
) -> Json<EndpointResponse<Recipe>> {
    let context = get_endpoint_context!(res);

    return match context
        .repository
        .recipe_collection
        .find_by_tokens(&ai_tokens.tokens)
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
    };
}
