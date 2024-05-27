use crate::endpoints::{get_response, EndpointResponse};
use crate::{
    endpoints::{rating::SERVICE, FAILED_RESPONSE, SUCCESSFUL_RESPONSE},
    models::{rating::List, ErrorResponse},
};
use reqwest::Method;
use salvo::oapi::extract::QueryParam;
use salvo::{http::StatusCode, oapi::endpoint, prelude::Json, Request, Response, Writer};
use tracing::error;

#[endpoint(
    parameters(
        ("parent_id" = String, description = "Rating id"),
        ("start" = i64, description = "Start value"),
        ("count" = i64, description = "Count value")
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
pub async fn get_rating_endpoint(
    req: &mut Request,
    res: &mut Response,
    start: QueryParam<u32, true>,
    count: QueryParam<u32, true>,
) -> Json<EndpointResponse<List>> {
    let uri = req.uri().path();
    let parts: Vec<&str> = uri.split('/').collect();
    let new_url = parts[3..].join("/");
    let url: String = format!("{SERVICE}/{new_url}");

    return match get_response::<[(&str, u32); 2], &str, List>(
        Method::GET,
        url,
        Some(&[("start", start.into_inner()), ("count", count.into_inner())]),
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
