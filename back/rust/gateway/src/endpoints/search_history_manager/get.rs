use crate::endpoints::search_history_manager::SERVICE;
use crate::endpoints::EndpointResponse;
use crate::endpoints::{get_response, FAILED_RESPONSE, SUCCESSFUL_RESPONSE};
use crate::models::message_history::History;
use crate::models::ErrorResponse;
use reqwest::{Method, StatusCode};
use salvo::oapi::endpoint;
use salvo::oapi::extract::QueryParam;
use salvo::prelude::Json;
use salvo::Writer;
use salvo::{Request, Response};
use tracing::error;

#[endpoint(
    parameters(
        ("user_id" = String, description = "Id of the user"),
        ("start" = i64, description = "Start value"),
        ("count" = i64, description = "Count value")
    ),
    responses
    (
        (
            status_code = StatusCode::OK,
            description = SUCCESSFUL_RESPONSE,
            body = History,
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
pub async fn get_search_history_endpoint(
    req: &mut Request,
    res: &mut Response,
    start: QueryParam<i64, true>,
    count: QueryParam<i64, true>,
) -> Json<EndpointResponse<History>> {
    let uri = req.uri().path();
    let parts: Vec<&str> = uri.split('/').collect();
    let new_url = parts[3..].join("/");
    let url: String = format!("{SERVICE}/{new_url}");

    return match get_response::<[(&str, i64); 2], &str, History>(
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
