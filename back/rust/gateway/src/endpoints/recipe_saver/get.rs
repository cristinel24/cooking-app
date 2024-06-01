use crate::endpoints::{get_response, EndpointResponse};
use crate::models::recipe::CardList;
use crate::{
    endpoints::{recipe_saver::SERVICE, FAILED_RESPONSE, SUCCESSFUL_RESPONSE},
    models::ErrorResponse,
};
use reqwest::Method;
use salvo::{http::StatusCode, oapi::endpoint, prelude::Json, Request, Response};
use tracing::error;

#[endpoint(
    parameters(
        ("user_id" = String, description = "User id"),
        ("start" = i64, Query, description = "Start value"),
        ("count" = i64, Query, description = "Count value"),
    ),
    responses
    (
        (
            status_code = StatusCode::OK,
            description = SUCCESSFUL_RESPONSE,
            body = CardList,
            example = json!(CardList::default())
        ),
        (
            status_code = StatusCode::INTERNAL_SERVER_ERROR,
            description = FAILED_RESPONSE,
            body = ErrorResponse,
            example = json!(ErrorResponse::default())
        ),
    )
)]
pub async fn get_saved_recipes(
    req: &mut Request,
    res: &mut Response,
) -> Json<EndpointResponse<CardList>> {
    let uri = req.uri().path();
    let parts: Vec<&str> = uri.split('/').collect();
    let new_url = parts[3..].join("/");
    let url: String = format!("{SERVICE}/{new_url}");

    return match get_response::<Vec<(&String, &String)>, &str, CardList>(
        Method::GET,
        url,
        Some(&req.queries().iter().collect()),
        None,
        Some(req.headers().clone()),
        false,
    )
    .await
    {
        Ok(item) => {
            if let EndpointResponse::Error((error_code, status_code)) = item {
                res.status_code(
                    StatusCode::from_u16(status_code).unwrap_or(StatusCode::INTERNAL_SERVER_ERROR),
                );
                Json(EndpointResponse::ServerError(error_code))
            } else {
                Json(item)
            }
        }
        Err(e) => {
            error!("{e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            Json(EndpointResponse::default())
        }
    };
}
