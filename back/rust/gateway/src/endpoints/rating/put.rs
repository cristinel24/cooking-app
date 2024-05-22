use super::SERVICE;
use crate::endpoints::{get_response, EndpointResponse};
use crate::{
    config::get_global_context,
    endpoints::{redirect, FAILED_RESPONSE, SUCCESSFUL_RESPONSE},
    get_redirect_url,
    models::{rating::Create, ErrorResponse},
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
        ("parent_id" = String, description = "Rating id")
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
pub async fn put_rating_endpoint(
    rating_create: JsonBody<Create>,
    req: &mut Request,
    res: &mut Response,
) -> Json<EndpointResponse<String>> {
    let uri = req.uri().to_string();
    let parts: Vec<&str> = uri.split('/').collect();
    let new_url = parts[1..].join("/");
    let url: String = get_redirect_url!(req, res, &new_url, SERVICE);
    let parent_id = req.param::<String>("parent_id").unwrap_or_default();

    return (get_response::<[(&str, String); 1], Create, String>(
        Method::PUT,
        url,
        Some(&[("parent_id", parent_id)]),
        Some(rating_create.into_inner()),
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
