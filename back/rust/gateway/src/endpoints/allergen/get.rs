use reqwest::{Method, StatusCode};
use salvo::oapi::endpoint;
use salvo::prelude::Json;
use salvo::{Request, Response, Writer};
use salvo::oapi::extract::QueryParam;
use crate::get_redirect_url;
use crate::models::ErrorResponse;
use crate::config::get_global_context;
use crate::endpoints::{redirect, SUCCESSFUL_RESPONSE, FAILED_RESPONSE, EndpointResponse, get_response};
use tracing::error;
use crate::endpoints::allergen::SERVICE;
use crate::models::allergens::Allergens;


#[endpoint(
    parameters(
        ("name" = String, description = "Name of Allergen"),
    ),
    responses
    (
        (
            status_code = StatusCode::OK,
            description = SUCCESSFUL_RESPONSE,
            body = String,
            example = json!(Allergens::default())
        ),
        (
            status_code = StatusCode::INTERNAL_SERVER_ERROR,
            description = FAILED_RESPONSE,
            body = ErrorResponse,
            example = json!(ErrorResponse::default())
        ),
    )
)]
pub async fn get_allergen_item(req: &mut Request, res: &mut Response, starting_with: QueryParam<String, true>) -> Json<EndpointResponse<Allergens>> {
    let url: String = get_redirect_url!(req, res, req.uri().path(), SERVICE);
    return (get_response::<[(&str, String); 1], &str, Allergens>(
        Method::GET,
        url,
        Some(&[("starting_with", starting_with.into_inner())]),
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