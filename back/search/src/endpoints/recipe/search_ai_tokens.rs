use crate::endpoints::recipe::{AiTokensPayload, RecipeResponsePayload};
use crate::endpoints::recipe::{ErrorResponse, RecipeResponse};
use crate::repository::extended_services::RecipeDatabaseOperations;
use crate::repository::get_context;
use crate::repository::models::recipe::ResponseRecipe;
use salvo::http::StatusCode;
use salvo::oapi::extract::JsonBody;
use salvo::prelude::{endpoint, Json, Writer};
use salvo::Response;
use tracing::error;

#[endpoint]
pub async fn search_ai_tokens(
    ai_tokens: JsonBody<AiTokensPayload>,
    res: &mut Response,
) -> Json<RecipeResponse> {
    let context = match get_context() {
        Ok(value) => value,
        Err(e) => {
            error!("Error: {e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            return Json(RecipeResponse::Error(ErrorResponse {
                message: e.to_string(),
            }));
        }
    };

    return match context
        .recipe_collection
        .find_by_tokens(&ai_tokens.tokens)
        .await
    {
        Ok(value) => {
            let size = value.len();
            Json(RecipeResponse::Success(RecipeResponsePayload {
                data: value.into_iter().map(|item| item.into()).collect(),
                count: size as u32,
            }))
        }
        Err(e) => {
            error!("Error: {e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            Json(RecipeResponse::Error(ErrorResponse {
                message: e.to_string(),
            }))
        }
    };
}
