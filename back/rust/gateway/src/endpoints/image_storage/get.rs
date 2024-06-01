use crate::endpoints::image_storage::{get_post_image, ImageResponse, SERVICE};
use crate::endpoints::{FAILED_RESPONSE, SUCCESSFUL_RESPONSE};
use crate::models::ErrorResponse;
use reqwest::{Method, StatusCode};
use salvo::fs::NamedFile;
use salvo::oapi::endpoint;
use salvo::prelude::Json;
use salvo::{Request, Response};
use tokio::fs;
use tracing::error;

#[endpoint(
    parameters(
        ("image_id" = String, description = "id of the image"),
    ),
    responses
    (
        (
            status_code = StatusCode::OK,
            description = SUCCESSFUL_RESPONSE,
            content_type = "image/png"
        ),
        (
            status_code = StatusCode::INTERNAL_SERVER_ERROR,
            description = FAILED_RESPONSE,
            body = ImageResponse,
            example = json!(ImageResponse::default())
        ),
    )
)]
pub async fn get_image(req: &mut Request, res: &mut Response) {
    let uri = req.uri().path();
    let parts: Vec<&str> = uri.split('/').collect();
    let new_url = parts[3..].join("/");
    let url = format!("{SERVICE}/{new_url}");

    match get_post_image(Method::GET, url, None, Some(req.headers().clone())).await {
        Ok(item) => match item {
            ImageResponse::ImageName(name) => {
                let file_name = format!("{name}.png");
                NamedFile::builder(file_name.clone())
                    .send(req.headers(), res)
                    .await;
                fs::remove_file(file_name).await.ok();
            }
            ImageResponse::Error((error_code, status_code)) => res
                .status_code(
                    StatusCode::from_u16(status_code).unwrap_or(StatusCode::INTERNAL_SERVER_ERROR),
                )
                .render(Json(error_code)),
            _ => res
                .status_code(StatusCode::INTERNAL_SERVER_ERROR)
                .render(Json(ErrorResponse::default())),
        },
        Err(e) => {
            error!("{e}");
            res.status_code(StatusCode::BAD_REQUEST)
                .render(Json(ErrorResponse::default()));
        }
    }
}
