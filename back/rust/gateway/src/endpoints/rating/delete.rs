use crate::{
    config::get_global_context,
    endpoints::{
        rating::{
            common::{body_rating_response, PutPatchType},
            EndpointResponse, SERVICE,
        },
        redirect, SUCCESSFUL_RESPONSE, FAILED_RESPONSE
    },
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
            example = json!(EndpointResponse::Error(ErrorResponse::default()))
        ),
    )
)]
pub async fn delete_rating_endpoint(
    req: &mut Request,
    res: &mut Response,
) -> Json<EndpointResponse> {
    let url: String = get_redirect_url!(req, res, SERVICE);
    let rating_id = req.param::<String>("rating_id").unwrap_or_default();

    return (body_rating_response(
        Method::DELETE,
        url.as_str(),
        &[("rating_id", rating_id)],
        PutPatchType::None,
        req.headers().clone(),
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
