use crate::endpoints::{get_response, EndpointResponse};
use crate::models::rating::Rating;
use crate::{
    endpoints::{rating_manager::SERVICE, FAILED_RESPONSE, SUCCESSFUL_RESPONSE},
    models::{rating::List, ErrorResponse},
};
use reqwest::Method;
use salvo::{http::StatusCode, oapi::endpoint, prelude::Json, Request, Response};
use tracing::error;

#[endpoint(
    parameters(
        ("parent_id" = String, description = "Rating id"),
    ),
    responses
    (
        (
            status_code = StatusCode::OK,
            description = SUCCESSFUL_RESPONSE,
            body = List,
            example = json!(List::default())
        ),
        (
            status_code = StatusCode::INTERNAL_SERVER_ERROR,
            description = FAILED_RESPONSE,
            body = ErrorResponse,
            example = json!(ErrorResponse::default())
        ),
    )
)]
pub async fn get_rating_by_id_endpoint(
    req: &mut Request,
    res: &mut Response,
) -> Json<EndpointResponse<Rating>> {
    let uri = req.uri().path();
    let parts: Vec<&str> = uri.split('/').collect();
    let new_url = parts[3..].join("/");
    let url: String = format!("{SERVICE}/{new_url}");

    return match get_response::<&str, &str, Rating>(
        Method::GET,
        url,
        None,
        None,
        Some(req.headers().clone()),
        false,
    )
    .await
    {
        Ok(item) => {
            if let EndpointResponse::Error((error_code, status_code)) = item {
                res.status_code(
                    StatusCode::from_u16(status_code).unwrap_or(StatusCode::INTERNAL_SERVER_ERROR),
                );
                Json(EndpointResponse::ServerError(error_code))
            } else {
                Json(item)
            }
        }
        Err(e) => {
            error!("{e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            Json(EndpointResponse::default())
        }
    };
}

