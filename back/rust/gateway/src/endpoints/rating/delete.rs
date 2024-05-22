use crate::endpoints::{get_response, EndpointResponse};
use crate::{
    config::get_global_context,
    endpoints::{rating::SERVICE, redirect, FAILED_RESPONSE, SUCCESSFUL_RESPONSE},
    get_redirect_url,
    models::ErrorResponse,
};
use reqwest::Method;
use salvo::{http::StatusCode, oapi::endpoint, prelude::Json, Request, Response};
use tracing::error;

#[endpoint(
    parameters(
        ("rating_id" = String, description = "Rating id")
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
pub async fn delete_rating_endpoint(
    req: &mut Request,
    res: &mut Response,
) -> Json<EndpointResponse<String>> {
    let uri = req.uri().to_string();
    let parts: Vec<&str> = uri.split('/').collect();
    let new_url = parts[1..].join("/");
    let url: String = get_redirect_url!(req, res, &new_url, SERVICE);
    let rating_id = req.param::<String>("rating_id").unwrap_or_default();

    return (get_response::<[(&str, String); 1], &str, String>(
        Method::DELETE,
        url,
        Some(&[("rating_id", rating_id)]),
        None,
        Some(req.headers().clone()),
        true,
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
