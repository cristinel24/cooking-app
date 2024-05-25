use crate::{
    context::get_global_context,
    endpoints::{common::normalize_recipe, EndpointResponse, ErrorCodes, ErrorResponse},
    get_endpoint_context,
    repository::{models::recipe::Recipe, service::recipe::Repository as RecipeRepository},
};
use salvo::{
    http::StatusCode,
    prelude::{endpoint, Json},
    Request, Response,
};
use tracing::error;

#[endpoint(
    parameters(
        ("title" = String, description = "Titlul retetei pe care o cauti")
    )
)]
pub async fn search_fuzz_title(
    req: &mut Request,
    res: &mut Response,
) -> Json<EndpointResponse<Recipe>> {
    let title = req.param::<String>("title").unwrap_or_default();
    let context = get_endpoint_context!(res);

    return match context
        .repository
        .recipe_collection
        .find_by_title(title)
        .await
    {
        Ok(mut value) => {
            for recipe in &mut value.data {
                if let Err(e) = normalize_recipe(recipe, &context.repository).await {
                    error!("Error: {e}");
                    res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
                    return Json(EndpointResponse::Error(ErrorResponse {
                        error_code: ErrorCodes::DbError as u32,
                    }));
                }
            }
            Json(EndpointResponse::Success(value))
        }
        Err(e) => {
            error!("Error: {e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            Json(EndpointResponse::Error(ErrorResponse {
                error_code: ErrorCodes::DbError as u32,
            }))
        }
    };
}
