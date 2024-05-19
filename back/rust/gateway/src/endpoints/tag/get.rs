use crate::config::get_global_context;
use crate::endpoints::redirect;
use crate::endpoints::tag::SERVICE;
use crate::endpoints::{get_response, EndpointResponse, FAILED_RESPONSE, SUCCESSFUL_RESPONSE};
use crate::get_redirect_url;
use crate::models::tags::Tags;
use crate::models::ErrorResponse;
use reqwest::{Method, StatusCode};
use salvo::oapi::endpoint;
use salvo::oapi::extract::QueryParam;
use salvo::prelude::Json;
use salvo::{Request, Response, Writer};
use tracing::error;

#[endpoint(
    responses
    (
        (
            status_code = StatusCode::OK,
            description = SUCCESSFUL_RESPONSE,
            body = String,
            example = json!(Tags::default())
        ),
        (
            status_code = StatusCode::INTERNAL_SERVER_ERROR,
            description = FAILED_RESPONSE,
            body = ErrorResponse,
            example = json!(ErrorResponse::default())
        ),
    )
)]
pub async fn get_tag_item(
    req: &mut Request,
    res: &mut Response,
    starting_with: QueryParam<String, true>,
) -> Json<EndpointResponse<Tags>> {
    let url: String = get_redirect_url!(req, res, req.uri().path(), SERVICE);
    return (get_response::<[(&str, String); 1], &str, Tags>(
        Method::GET,
        url,
        Some(&[("starting_with", starting_with.into_inner())]),
        None,
        None,
        false,
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
