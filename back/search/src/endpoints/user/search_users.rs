use crate::endpoints::{EndpointResponse, ErrorResponse};
use crate::get_context;
use crate::repository::extended_services::UserDatabaseOperations;
use crate::repository::get_context;
use crate::repository::models::user::User;
use salvo::http::StatusCode;
use salvo::prelude::{endpoint, Json};
use salvo::{Request, Response};
use tracing::error;

#[endpoint(
    parameters
    (
        ("name" = String, description="name")
    )
)]
pub async fn search_users(res: &mut Response, req: &mut Request) -> Json<EndpointResponse<User>> {
    let id = req.param::<String>("name").unwrap_or_default();
    let context = get_context!(res);

    return match context.user_collection.find_by_name(id).await {
        Ok(value) => Json(EndpointResponse::Success(value)),
        Err(e) => {
            error!("Error: {e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            Json(EndpointResponse::Error(ErrorResponse {
                message: e.to_string(),
            }))
        }
    };
}
