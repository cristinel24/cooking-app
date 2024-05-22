use crate::config::get_global_context;
use crate::endpoints::{get_response, recipe_saver::SERVICE, FAILED_RESPONSE, SUCCESSFUL_RESPONSE};
use crate::endpoints::{redirect, EndpointResponse};
use crate::get_redirect_url;
use crate::models::recipe::SaveDeleteRequest;
use crate::models::ErrorResponse;
use reqwest::{Method, StatusCode};
use salvo::oapi::endpoint;
use salvo::oapi::extract::JsonBody;
use salvo::prelude::Json;
use salvo::{Request, Response, Writer};
use tracing::error;

#[endpoint(
    parameters(
        ("user_id" = String, description = "Id of the user")
    ),
    responses
    (
        (
            status_code = StatusCode::OK,
            description = SUCCESSFUL_RESPONSE,
            body = SaveDeleteRequest,
            example = json!(SaveDeleteRequest::default())
        ),
        (
            status_code = StatusCode::INTERNAL_SERVER_ERROR,
            description = FAILED_RESPONSE,
            body = ErrorResponse,
            example = json!(ErrorResponse::default())
        ),
    )
)]
pub async fn put_recipe(
    req: &mut Request,
    res: &mut Response,
    data: JsonBody<SaveDeleteRequest>,
) -> Json<EndpointResponse<String>> {
    let uri = req.uri().to_string();
    let parts: Vec<&str> = uri.split('/').collect();
    let new_url = parts[2..].join("/");
    let url: String = get_redirect_url!(req, res, &new_url, SERVICE);

    return (get_response::<&str, SaveDeleteRequest, String>(
        Method::PUT,
        url,
        None,
        Some(data.into_inner()),
        Some(req.headers().clone()),
        true,
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
