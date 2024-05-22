use bytes::Bytes;
use crate::config::get_global_context;
use crate::endpoints::{FAILED_RESPONSE, SUCCESSFUL_RESPONSE};
use crate::endpoints::{redirect, EndpointResponse};
use crate::get_redirect_url;
use crate::models::search::Query;
use crate::models::ErrorResponse;
use reqwest::{Client, Method, StatusCode};
use salvo::oapi::endpoint;
use salvo::oapi::extract::JsonBody;
use salvo::prelude::Json;
use salvo::{Request, Response};
use serde::Serialize;
use tracing::error;
use crate::endpoints::image_storage::{get_put_image, ImageResponse, SERVICE};

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
pub async fn get_image(
    req: &mut Request,
    res: &mut Response,
) -> Json<ImageResponse> {
    let uri = req.uri().to_string();
    let parts: Vec<&str> = uri.split('/').collect();
    let new_url = parts[2..].join("/");
    let context = match get_global_context() {
        Ok(value) => value,
        Err(e) => {
            error!("Error: {e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            return Json(ImageResponse::Error(ErrorResponse::default()));
        }
    };
    let Ok(url) = redirect(context, &new_url, SERVICE) else {
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            return Json(ImageResponse::Error(ErrorResponse::default()));
        };

    println!("url: {url}");

    return (get_put_image(
        Method::GET,
        url,
        None,
        true
    ).await).map_or_else(
        |_| {
            res.status_code(StatusCode::BAD_REQUEST);
            Json(ImageResponse::Error(ErrorResponse::default()))
        },
        Json,
    );

}