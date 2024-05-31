use crate::endpoints::user_retriever::SERVICE;
use crate::endpoints::{get_response, EndpointResponse, FAILED_RESPONSE, SUCCESSFUL_RESPONSE};
use crate::models::user::UserCard;
use reqwest::{Method, StatusCode};
use salvo::oapi::endpoint;
use salvo::prelude::Json;
use salvo::{Request, Response};

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
            body = UserCard,
            example = json!(UserCard::default())
        ),
        (
            status_code = StatusCode::INTERNAL_SERVER_ERROR,
            description = FAILED_RESPONSE,
            body = ErrorResponse,
            example = json!(ErrorResponse::default())
        ),
    )
)]
pub async fn get_user_card_item(
    req: &mut Request,
    res: &mut Response,
) -> Json<EndpointResponse<UserCard>> {
    let uri = req.uri().path();
    let parts: Vec<&str> = uri.split('/').collect();
    let new_url = parts[3..].join("/");
    let url: String = format!("{SERVICE}/{new_url}");

    return match get_response::<&str, &str, UserCard>(
        Method::GET,
        url,
        None,
        None,
        Some(req.headers().clone()),
        false,
    )
    .await {
        Ok(item) => {
            if let EndpointResponse::Error((error_code, status_code)) = item {
                res.status_code(StatusCode::from_u16(status_code).unwrap_or(StatusCode::INTERNAL_SERVER_ERROR));
                Json(EndpointResponse::ServerError(error_code))
            } else {
                Json(item)
            }
        },
        Err(e) => {
            error!("{e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            Json(EndpointResponse::default())
        }
    }
}
