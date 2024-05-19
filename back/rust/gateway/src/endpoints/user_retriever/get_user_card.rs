use crate::endpoints::user_retriever::SERVICE;
use crate::endpoints::{get_response, EndpointResponse, SUCCESSFUL_RESPONSE, FAILED_RESPONSE};
use crate::get_redirect_url;
use crate::models::user::CardData;
use reqwest::{Method, StatusCode};
use salvo::prelude::Json;
use salvo::{Request, Response};
use salvo::oapi::endpoint;

use crate::config::get_global_context;
use crate::endpoints::redirect;
use crate::models::ErrorResponse;
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
            body = CardData,
            example = json!(CardData::default())
        ),
        (
            status_code = StatusCode::INTERNAL_SERVER_ERROR,
            description = FAILED_RESPONSE,
            body = ErrorResponse,
            example = json!(ErrorResponse::default())
        ),
    )
)]
pub async fn get_user_card_item(
    req: &mut Request,
    res: &mut Response,
) -> Json<EndpointResponse<CardData>> {
    let url: String = get_redirect_url!(req, res, req.uri().path(), SERVICE);

    return (get_response::<&str, &str, CardData>(Method::GET, url, None, None, None, true).await)
        .map_or_else(
            |_| {
                res.status_code(StatusCode::BAD_REQUEST);
                Json(EndpointResponse::Error(ErrorResponse::default()))
            },
            Json,
        );
}
