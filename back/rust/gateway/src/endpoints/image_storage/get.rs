use crate::endpoints::image_storage::{get_put_image, ImageResponse, SERVICE};
use crate::endpoints::{FAILED_RESPONSE, SUCCESSFUL_RESPONSE};
use crate::models::ErrorResponse;
use reqwest::{Method, StatusCode};
use salvo::oapi::endpoint;
use salvo::prelude::Json;
use salvo::{Request, Response};

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
pub async fn get_image(req: &mut Request, res: &mut Response) -> Json<ImageResponse> {
    let uri = req.uri().path();
    let parts: Vec<&str> = uri.split('/').collect();
    let new_url = parts[3..].join("/");
    let url = format!("{SERVICE}/{new_url}");

    return (get_put_image(Method::GET, url, None, true).await).map_or_else(
        |_| {
            res.status_code(StatusCode::BAD_REQUEST);
            Json(ImageResponse::Error(ErrorResponse::default()))
        },
        Json,
    );
}
