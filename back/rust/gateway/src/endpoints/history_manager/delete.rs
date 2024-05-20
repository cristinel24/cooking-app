use crate::config::get_global_context;
use crate::endpoints::history_manager::SERVICE;
use crate::endpoints::{get_response, FAILED_RESPONSE, SUCCESSFUL_RESPONSE};
use crate::endpoints::{redirect, EndpointResponse};
use crate::get_redirect_url;
use crate::models::ErrorResponse;
use reqwest::{Method, StatusCode};
use salvo::oapi::endpoint;
use salvo::prelude::Json;
use salvo::{Request, Response};
use tracing::error;

#[endpoint(
    parameters(
        ("user_id" = String, description = "Id of the user"),
    ),
    responses
    (
        (
            status_code = StatusCode::OK,
            description = SUCCESSFUL_RESPONSE,
            body = String,
            example = json!("null")
        ),
        (
            status_code = StatusCode::INTERNAL_SERVER_ERROR,
            description = FAILED_RESPONSE,
            body = ErrorResponse,
            example = json!(ErrorResponse::default())
        ),
    )
)]
pub async fn delete_item_search_history(
    req: &mut Request,
    res: &mut Response,
) -> Json<EndpointResponse<String>> {
    let url: String = get_redirect_url!(req, res, req.uri().path(), SERVICE);

    return (get_response::<&str, &str, String>(
        Method::DELETE,
        url,
        None,
        None,
        Some(req.headers().clone()),
        false,
    )
    .await)
        .map_or_else(
            |_| {
                res.status_code(StatusCode::BAD_REQUEST);
                Json(EndpointResponse::Error(ErrorResponse::default()))
            },
            Json,
        );
}
