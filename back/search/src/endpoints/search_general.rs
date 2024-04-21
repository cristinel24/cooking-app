use crate::repository::get_context;
use salvo::http::StatusCode;
use salvo::oapi::extract::JsonBody;
use salvo::prelude::{endpoint, Json, Writer};
use salvo::Response;
use tracing::error;
use crate::endpoints::{EndpointResponse, ErrorResponse, InputPayload, INTERNAL_SERVER_ERROR};
use crate::repository::extended_services::{AllergenDatabaseOperations, RecipeDatabaseOperations, TagDatabaseOperations};


#[endpoint]
pub async fn search_general(payload: JsonBody<InputPayload>, res: &mut Response) -> Json<EndpointResponse> {
    
    let context = match get_context() {
        Ok(value) => value,
        Err(e) => {
            error!("Error: {e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            return Json(EndpointResponse::Error(ErrorResponse {
                message: e.to_string(),
            }));
        }
    };

    let recipes = match context
        .recipe_collection
        .search(payload.into_inner())
        .await
    {
        Ok(mut value) => {
            if value.data.is_empty() {
                return Json(EndpointResponse::default());
            }

            for recipe in value.data.iter_mut() {
                let top_tags = match context
                    .tag_collection
                    .filter_top_x_tags(recipe.tags.clone(), crate::endpoints::recipe::TOP)
                    .await
                {
                    Ok(value) => value,
                    Err(_) => {
                        res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
                        return Json(EndpointResponse::Error(ErrorResponse {
                            message: INTERNAL_SERVER_ERROR.to_string(),
                        }));
                    }
                };
                if let Some(top) = top_tags {
                    recipe.tags = top;
                }
                let top_tags = match context
                    .allergen_collection
                    .filter_top_x_allergens(recipe.allergens.clone(), crate::endpoints::recipe::TOP)
                    .await
                {
                    Ok(value) => value,
                    Err(_) => {
                        res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
                        return Json(EndpointResponse::Error(ErrorResponse {
                            message: INTERNAL_SERVER_ERROR.to_string(),
                        }));
                    }
                };
                if let Some(top) = top_tags {
                    recipe.allergens = top;
                }
            }

            value
        }
        Err(e) => {
            error!("Error: {e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            return Json(EndpointResponse::Error(ErrorResponse {
                message: e.to_string(),
            }))
        }
    };

    Json(EndpointResponse::default())
}
