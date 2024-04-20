use crate::endpoints::recipe::{ErrorResponse, RecipeResponse, TOP};
use crate::repository::extended_services::{AllergenDatabaseOperations, RecipeDatabaseOperations, TagDatabaseOperations};
use crate::repository::get_context;
use salvo::http::StatusCode;
use salvo::prelude::{endpoint, Json};
use salvo::{Request, Response};
use tracing::error;
use crate::endpoints::INTERNAL_SERVER_ERROR;


#[endpoint(
    parameters(
        ("title" = String, description = "Titlul retetei pe care o cauti")
    )
)]
pub async fn search_fuzz_title(req: &mut Request, res: &mut Response) -> Json<RecipeResponse> {
    let title = req.param::<String>("title").unwrap_or_default();
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
        .find_by_title(title)
        .await
    {
        Ok(mut value) => {
            if value.data.is_empty() {
                return Json(RecipeResponse::default());
            }
            for recipe in value.data.iter_mut() {
                let top_tags = match context
                    .tag_collection
                    .filter_top_x_tags(recipe.tags.clone(), TOP)
                    .await
                {
                    Ok(value) => value,
                    Err(_) => {
                        res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
                        return Json(RecipeResponse::Error(ErrorResponse {
                            message: INTERNAL_SERVER_ERROR.to_string(),
                        }));
                    }
                };
                if let Some(top) = top_tags {
                    recipe.tags = top;
                }
                let top_tags = match context
                    .allergen_collection
                    .filter_top_x_allergens(recipe.allergens.clone(), TOP)
                    .await
                {
                    Ok(value) => value,
                    Err(_) => {
                        res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
                        return Json(RecipeResponse::Error(ErrorResponse {
                            message: INTERNAL_SERVER_ERROR.to_string(),
                        }));
                    }
                };
                if let Some(top) = top_tags {
                    recipe.allergens = top;
                }
            }
            Json(RecipeResponse::Success(value))
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
