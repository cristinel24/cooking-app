use crate::endpoints::ai::SERVICE;
use crate::endpoints::{get_response, EndpointResponse, FAILED_RESPONSE, SUCCESSFUL_RESPONSE};
use crate::models::ai::{TokenizeRequest, TokenizeResponse};
use crate::models::ErrorResponse;
use reqwest::{Method, StatusCode};
use salvo::oapi::endpoint;
use salvo::oapi::extract::JsonBody;
use salvo::prelude::Json;
use salvo::{Request, Response, Writer};
use tracing::error;

#[endpoint(
    responses
    (
        (
            status_code = StatusCode::OK,
            description = SUCCESSFUL_RESPONSE,
            body = TokenizeResponse,
            example = json!(TokenizeResponse::default())
        ),
        (
            status_code = StatusCode::INTERNAL_SERVER_ERROR,
            description = FAILED_RESPONSE,
            body = ErrorResponse,
            example = json!(ErrorResponse::default())
        ),
    )
)]
pub async fn replace_ingredient(
    req: &mut Request,
    res: &mut Response,
    body: JsonBody<TokenizeRequest>,
) -> Json<EndpointResponse<TokenizeResponse>> {
    let uri = req.uri().path();
    let parts: Vec<&str> = uri.split('/').collect();
    let new_url = parts[3..].join("/");
    let url: String = format!("{SERVICE}/{new_url}");
    return (get_response::<&str, TokenizeRequest, TokenizeResponse>(
        Method::POST,
        url,
        None,
        Some(body.into_inner()),
        Some(req.headers().clone()),
        false,
    )
    .await)
        .map_or_else(
            |e| {
                error!("{e}");
                res.status_code(StatusCode::BAD_REQUEST);
                Json(EndpointResponse::Error(ErrorResponse::default()))
            },
            Json,
        );
}
