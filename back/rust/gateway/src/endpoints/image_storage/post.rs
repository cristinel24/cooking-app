use crate::endpoints::image_storage::{get_post_image, ImageResponse, SERVICE};

use crate::endpoints::{FAILED_RESPONSE, SUCCESSFUL_RESPONSE};
use crate::models::image_storage::UrlResponse;
use crate::models::ErrorResponse;
use reqwest::{Method, StatusCode};
use salvo::oapi::endpoint;
use salvo::prelude::Json;
use salvo::{Request, Response};
use serde_json::Value;
use tracing::error;

#[endpoint(
    request_body(content = Value, content_type = "image/png"),
    responses
    (
        (
            status_code = StatusCode::OK,
            description = SUCCESSFUL_RESPONSE,
            body = UrlResponse,
            example = json!(UrlResponse::default())
        ),
        (
            status_code = StatusCode::INTERNAL_SERVER_ERROR,
            description = FAILED_RESPONSE,
            body = ErrorResponse,
            example = json!(ErrorResponse::default())
        ),
    )
)]
pub async fn post_image(req: &mut Request, res: &mut Response) -> Json<ImageResponse> {
    let url = SERVICE.to_string();

    let bytes = match req.payload().await {
        Ok(value) => value.clone(),
        Err(_) => return Json(ImageResponse::ServerError(ErrorResponse::default())),
    };

    match get_post_image(Method::POST, url, Some(bytes)).await {
        Ok(item) => {
            if let ImageResponse::Error((error_code, status_code)) = item {
                res.status_code(
                    StatusCode::from_u16(status_code).unwrap_or(StatusCode::INTERNAL_SERVER_ERROR),
                );
                Json(ImageResponse::ServerError(error_code))
            } else {
                Json(item)
            }
        }
        Err(e) => {
            error!("{e}");
            res.status_code(StatusCode::BAD_REQUEST);
            Json(ImageResponse::ServerError(ErrorResponse::default()))
        }
    }
}
