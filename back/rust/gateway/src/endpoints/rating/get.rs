use crate::{
    config::get_global_context,
    endpoints::{
        rating::SERVICE,
        redirect, SUCCESSFUL_RESPONSE, FAILED_RESPONSE
    },
    get_redirect_url,
    models::{rating::List, ErrorResponse},
};
use reqwest::Method;
use salvo::oapi::extract::QueryParam;
use salvo::{http::StatusCode, oapi::endpoint, prelude::Json, Request, Response, Writer};
use tracing::error;
use crate::endpoints::{EndpointResponse, get_response};


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
    let url: String = get_redirect_url!(req, res, req.uri().path(), SERVICE);

    return (get_response::<[(&str, u32); 2], &str, List>(
        Method::GET,
        url,
        Some(&[("start", start.into_inner()), ("count", count.into_inner())]),
        None,
        None,
        false
    )
    .await)
        .map_or_else(
            |_| {
                res.status_code(StatusCode::BAD_REQUEST);
                Json(EndpointResponse::Error(ErrorResponse::default()))
            },
            Json,
        );
}
