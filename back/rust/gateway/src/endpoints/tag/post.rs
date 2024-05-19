use reqwest::{Method, StatusCode};
use salvo::oapi::endpoint;
use salvo::prelude::Json;
use salvo::{Request, Response};
use crate::get_redirect_url;
use crate::models::ErrorResponse;
use crate::config::get_global_context;
use crate::endpoints::{redirect, SUCCESSFUL_RESPONSE, FAILED_RESPONSE, EndpointResponse, get_response};
use tracing::error;
use crate::endpoints::tag::SERVICE;


#[endpoint(
    parameters(
        ("name" = String, description = "Name of Tag"),
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
pub async fn post_tag_item(req: &mut Request, res: &mut Response) -> Json<EndpointResponse<String>> {
    let url: String = get_redirect_url!(req, res, req.uri().path(), SERVICE);
    return (get_response::<&str, &str, String>(
        Method::POST,
        url,
        None,
        None,
        None,
        true
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