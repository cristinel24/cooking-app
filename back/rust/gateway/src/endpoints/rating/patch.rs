use super::SERVICE;
use crate::endpoints::{get_response, EndpointResponse};
use crate::{
    config::get_global_context,
    endpoints::{redirect, FAILED_RESPONSE, SUCCESSFUL_RESPONSE},
    get_redirect_url,
    models::{rating::Update, ErrorResponse},
};
use reqwest::{Method, StatusCode};
use salvo::{
    oapi::{endpoint, extract::JsonBody},
    prelude::Json,
    Request, Response, Writer,
};
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
pub async fn patch_rating_endpoint(
    rating_update: JsonBody<Update>,
    req: &mut Request,
    res: &mut Response,
) -> Json<EndpointResponse<String>> {
    let uri = req.uri().to_string();
    let parts: Vec<&str> = uri.split('/').collect();
    let new_url = parts[1..].join("/");
    let url: String = get_redirect_url!(req, res, &new_url, SERVICE);
    return (get_response::<&str, Update, String>(
        Method::PATCH,
        url,
        None,
        Some(rating_update.into_inner()),
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
