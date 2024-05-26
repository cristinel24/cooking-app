use crate::endpoints::image_storage::{get_put_image, ImageResponse, SERVICE};

use crate::endpoints::{FAILED_RESPONSE, SUCCESSFUL_RESPONSE};
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
            body = String,
            example = json!("null")
        ),
        (
            status_code = StatusCode::INTERNAL_SERVER_ERROR,
            description = FAILED_RESPONSE,
            body = ImageResponse,
            example = json!(ImageResponse::default())
        ),
    )
)]
pub async fn put_image(req: &mut Request, res: &mut Response) -> Json<ImageResponse> {
    let uri = req.uri().path();
    let parts: Vec<&str> = uri.split('/').collect();
    let new_url = parts[3..].join("/");
    let url = format!("{SERVICE}/{new_url}");

    let bytes = match req.payload().await {
        Ok(value) => value.clone(),
        Err(_) => return Json(ImageResponse::Error(ErrorResponse::default())),
    };

    return (get_put_image(Method::PUT, format!("http://{url}"), Some(bytes), true).await)
        .map_or_else(
            |e| {
                error!("{e}");
                res.status_code(StatusCode::BAD_REQUEST);
                Json(ImageResponse::Error(ErrorResponse::default()))
            },
            Json,
        );
}
