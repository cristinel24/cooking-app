use super::SERVICE;
use crate::endpoints::{get_response, EndpointResponse};
use crate::{
    endpoints::{FAILED_RESPONSE, SUCCESSFUL_RESPONSE},
    models::{rating::Update, ErrorResponse},
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
            example = json!(ErrorResponse::default())
        ),
    )
)]
pub async fn patch_rating_endpoint(
    rating_update: JsonBody<Update>,
    req: &mut Request,
    res: &mut Response,
) -> Json<EndpointResponse<String>> {
    let uri = req.uri().path();
    let parts: Vec<&str> = uri.split('/').collect();
    let new_url = parts[3..].join("/");
    let url: String = format!("{SERVICE}/{new_url}");
    return match get_response::<&str, Update, String>(
        Method::PATCH,
        url,
        None,
        Some(rating_update.into_inner()),
        Some(req.headers().clone()),
        true,
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
