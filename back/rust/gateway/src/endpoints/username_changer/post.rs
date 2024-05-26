use crate::endpoints::username_changer::SERVICE;
use crate::endpoints::{get_response, EndpointResponse, FAILED_RESPONSE, SUCCESSFUL_RESPONSE};
use crate::models::username_changer::ChangeName;
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
            body = String,
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
pub async fn change_username(
    req: &mut Request,
    res: &mut Response,
    data: JsonBody<ChangeName>,
) -> Json<EndpointResponse<String>> {
    let url: String = SERVICE.to_string();

    return (get_response::<&str, ChangeName, String>(
        Method::POST,
        url,
        None,
        Some(data.into_inner()),
        Some(req.headers().clone()),
        true,
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
