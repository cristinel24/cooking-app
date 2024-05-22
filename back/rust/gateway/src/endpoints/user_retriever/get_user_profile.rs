use crate::endpoints::user_retriever::SERVICE;
use crate::endpoints::{get_response, EndpointResponse, FAILED_RESPONSE, SUCCESSFUL_RESPONSE};
use crate::get_redirect_url;
use crate::models::user::FullData;
use reqwest::{Method, StatusCode};
use salvo::oapi::endpoint;
use salvo::prelude::Json;
use salvo::{Request, Response};

use crate::config::get_global_context;
use crate::endpoints::redirect;
use crate::models::ErrorResponse;
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
            body = FullData,
            example = json!(FullData::default())
        ),
        (
            status_code = StatusCode::INTERNAL_SERVER_ERROR,
            description = FAILED_RESPONSE,
            body = ErrorResponse,
            example = json!(ErrorResponse::default())
        ),
    )
)]
pub async fn get_user_profile_item(
    req: &mut Request,
    res: &mut Response,
) -> Json<EndpointResponse<FullData>> {
    let uri = req.uri().to_string();
    let parts: Vec<&str> = uri.split('/').collect();
    let new_url = parts[1..].join("/");
    let url: String = get_redirect_url!(req, res, &new_url, SERVICE);

    return (get_response::<&str, &str, FullData>(
        Method::GET,
        url,
        None,
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
