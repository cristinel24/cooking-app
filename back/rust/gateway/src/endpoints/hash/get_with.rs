use crate::config::get_global_context;
use crate::endpoints::hash::SERVICE;
use crate::endpoints::redirect;
use crate::endpoints::{get_response, EndpointResponse, FAILED_RESPONSE, SUCCESSFUL_RESPONSE};
use crate::get_redirect_url;
use crate::models::hash::AlgorithmName;
use crate::models::ErrorResponse;
use reqwest::Method;
use salvo::http::StatusCode;
use salvo::oapi::endpoint;
use salvo::oapi::extract::QueryParam;
use salvo::prelude::Json;
use salvo::{Request, Response, Writer};
use tracing::error;

#[endpoint(
    parameters(
        ("target" = String, description = "Target"),
        ("hash_algorithm_name" = String, description = "Hash Algorithm Name")
    ),
    responses
    (
        (
            status_code = StatusCode::OK,
            description = SUCCESSFUL_RESPONSE,
            body = AlgorithmName,
            example = json!(AlgorithmName::default())
        ),
        (
            status_code = StatusCode::INTERNAL_SERVER_ERROR,
            description = FAILED_RESPONSE,
            body = ErrorResponse,
            example = json!(ErrorResponse::default())
        ),
    )
)]
pub async fn get_hash_with(
    req: &mut Request,
    res: &mut Response,
    salt: QueryParam<String, true>,
) -> Json<EndpointResponse<AlgorithmName>> {
    let uri = req.uri().to_string();
    let mut parts: Vec<&str> = uri.split('/').collect();
    if !parts.is_empty() {
        parts.remove(1);
    }
    let new_url = parts.join("/");
    let url: String = get_redirect_url!(req, res, &new_url, SERVICE);

    return (get_response::<[(&str, String); 1], &str, AlgorithmName>(
        Method::GET,
        url,
        Some(&[("salt", salt.into_inner())]),
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
