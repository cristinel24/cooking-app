use crate::config::get_global_context;
use crate::endpoints::{
    get_response, redirect, EndpointResponse, FAILED_RESPONSE, SUCCESSFUL_RESPONSE,
};
use crate::get_redirect_url;
use crate::models::ErrorResponse;
use reqwest::{Method, StatusCode};
use salvo::oapi::endpoint;
use salvo::prelude::Json;
use salvo::{Request, Response, Writer};
use salvo::oapi::extract::JsonBody;
use tracing::error;
use crate::endpoints::email::SERVICE;
use crate::models::email::RequestChange;

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
    request_change_data: JsonBody<RequestChange>
) -> Json<EndpointResponse<String>> {
    let url: String = get_redirect_url!(req, res, req.uri().path(), SERVICE);
    return (get_response::<&str, RequestChange, String>(Method::POST, url, None, Some(request_change_data.into_inner()), None, true).await)
        .map_or_else(
            |_| {
                res.status_code(StatusCode::BAD_REQUEST);
                Json(EndpointResponse::Error(ErrorResponse::default()))
            },
            Json,
        );
}
