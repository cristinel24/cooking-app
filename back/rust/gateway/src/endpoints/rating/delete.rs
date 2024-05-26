use crate::endpoints::{get_response, EndpointResponse};
use crate::{

    endpoints::{rating::SERVICE, FAILED_RESPONSE, SUCCESSFUL_RESPONSE},

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
    let uri = req.uri().path();
    let parts: Vec<&str> = uri.split('/').collect();
    let new_url = parts[3..].join("/");
    let url: String = format!("{SERVICE}/{new_url}");

    return (get_response::<&str, &str, String>(
        Method::DELETE,
        url,
        None,
        None,
        Some(req.headers().clone()),
        true,
    )
    .await)
        .map_or_else(
            |e| {
                error!("{e}");
                res.status_code(StatusCode::BAD_REQUEST);
                Json(EndpointResponse::Error(ErrorResponse::default()))
            },
            Json,
        );
}
