use crate::endpoints::follow_manager::SERVICE;
use crate::endpoints::{get_response, EndpointResponse, FAILED_RESPONSE, SUCCESSFUL_RESPONSE};
use crate::models::follow_manager::FollowingCount;
use crate::models::ErrorResponse;
use reqwest::{Method, StatusCode};
use salvo::oapi::endpoint;
use salvo::prelude::Json;
use salvo::{Request, Response};
use tracing::error;

#[endpoint(
    parameters(
        ("user_id" = String, description = "Id of the user")
    ),
    responses
    (
        (
            status_code = StatusCode::OK,
            description = SUCCESSFUL_RESPONSE,
            body = FollowingCount,
            example = json!(FollowingCount::default())
        ),
        (
            status_code = StatusCode::INTERNAL_SERVER_ERROR,
            description = FAILED_RESPONSE,
            body = ErrorResponse,
            example = json!(ErrorResponse::default())
        ),
    )
)]
pub async fn get_user_following_count(
    req: &mut Request,
    res: &mut Response,
) -> Json<EndpointResponse<FollowingCount>> {
    let uri = req.uri().path();
    let parts: Vec<&str> = uri.split('/').collect();
    let new_url = parts[3..].join("/");
    let url: String = format!("{SERVICE}/{new_url}");

    return (get_response::<&str, &str, FollowingCount>(
        Method::GET,
        url,
        None,
        None,
        Some(req.headers().clone()),
        false,
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
