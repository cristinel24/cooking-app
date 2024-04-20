use crate::endpoints::user::{ErrorResponse, UserResponse, UserResponsePayload};
use crate::repository::extended_services::UserDatabaseOperations;
use crate::repository::get_context;
use salvo::http::StatusCode;
use salvo::oapi::extract::JsonBody;
use salvo::prelude::{endpoint, Json, Writer};
use salvo::{Request, Response};
use tracing::error;

#[endpoint(parameters(("display_name" = String, description="display_name")))]
pub async fn search_user(res: &mut Response, req: &mut Request) -> Json<UserResponse> {
    let id = req.param::<String>("display_name").unwrap_or_default();
    let context = match get_context() {
        Ok(value) => value,
        Err(e) => {
            error!("Error: {e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            return Json(UserResponse::Error(ErrorResponse {
                message: e.to_string(),
            }));
        }
    };
    return match context.user_collection.find_by_display_name(&id).await {
        Ok(value) => Json(UserResponse::Success(value)),
        Err(e) => {
            error!("Error: {e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            Json(UserResponse::Error(ErrorResponse {
                message: e.to_string(),
            }))
        }
    };
}
