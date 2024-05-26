use crate::endpoints::password_changer::SERVICE;
use crate::endpoints::{get_response, EndpointResponse, FAILED_RESPONSE, SUCCESSFUL_RESPONSE};
use crate::models::login::Success;
use crate::models::password_changer::PassChange;
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
            body = Success,
            example = json!(Success::default())
        ),
        (
            status_code = StatusCode::INTERNAL_SERVER_ERROR,
            description = FAILED_RESPONSE,
            body = ErrorResponse,
            example = json!(ErrorResponse::default())
        ),
    )
)]
pub async fn pass_change(
    req: &mut Request,
    res: &mut Response,
    data: JsonBody<PassChange>,
) -> Json<EndpointResponse<String>> {
    let url: String = SERVICE.to_string();

    return (get_response::<&str, PassChange, String>(
        Method::PUT,
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
