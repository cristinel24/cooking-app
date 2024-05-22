use crate::config::get_global_context;
use crate::endpoints::email::SERVICE;
use crate::endpoints::{
    get_response, redirect, EndpointResponse, FAILED_RESPONSE, SUCCESSFUL_RESPONSE,
};
use crate::get_redirect_url;
use crate::models::email::RequestChange;
use crate::models::ErrorResponse;
use reqwest::{Method, StatusCode};
use salvo::oapi::endpoint;
use salvo::oapi::extract::JsonBody;
use salvo::prelude::Json;
use salvo::{Request, Response, Writer};
use tracing::error;

#[endpoint(
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
pub async fn request_change(
    req: &mut Request,
    res: &mut Response,
    request_change_data: JsonBody<RequestChange>,
) -> Json<EndpointResponse<String>> {
    let uri = req.uri().to_string();
    let parts: Vec<&str> = uri.split('/').collect();
    let new_url = parts[1..].join("/");
    let url: String = get_redirect_url!(req, res, &new_url, SERVICE);
    return (get_response::<&str, RequestChange, String>(
        Method::POST,
        url,
        None,
        Some(request_change_data.into_inner()),
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
