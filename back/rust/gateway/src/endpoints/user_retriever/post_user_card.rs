use crate::endpoints::user_retriever::SERVICE;
use crate::endpoints::{get_response, EndpointResponse, FAILED_RESPONSE, SUCCESSFUL_RESPONSE};
use crate::get_redirect_url;
use crate::models::user::Cards;
use reqwest::{Method, StatusCode};
use salvo::oapi::endpoint;
use salvo::prelude::Json;
use salvo::{Request, Response};

use crate::config::get_global_context;
use crate::endpoints::redirect;
use crate::models::ErrorResponse;
use tracing::error;

#[endpoint(
    responses
    (
        (
            status_code = StatusCode::OK,
            description = SUCCESSFUL_RESPONSE,
            body = Cards,
            example = json!(Cards::default())
        ),
        (
            status_code = StatusCode::INTERNAL_SERVER_ERROR,
            description = FAILED_RESPONSE,
            body = ErrorResponse,
            example = json!(ErrorResponse::default())
        ),
    )
)]
pub async fn post_user_card_item(
    req: &mut Request,
    res: &mut Response,
) -> Json<EndpointResponse<Cards>> {
    let uri = req.uri().to_string();
    let mut parts: Vec<&str> = uri.split('/').collect();
    if !parts.is_empty() {
        parts.remove(1);
    }
    let new_url = parts.join("/");
    let url: String = get_redirect_url!(req, res, &new_url, SERVICE);

    return (get_response::<&str, &str, Cards>(Method::POST, url, None, None, None, true).await)
        .map_or_else(
            |_| {
                res.status_code(StatusCode::BAD_REQUEST);
                Json(EndpointResponse::Error(ErrorResponse::default()))
            },
            Json,
        );
}
