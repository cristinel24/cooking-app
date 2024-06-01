use crate::endpoints::{
    get_response, search::SERVICE, EndpointResponse, FAILED_RESPONSE, SUCCESSFUL_RESPONSE,
};
use crate::models::recipe::RecipeCardList;
use crate::models::search::SearchWithAiBody;
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
            body = RecipeCardList,
            example = json!(RecipeCardList::default())
        ),
        (
            status_code = StatusCode::INTERNAL_SERVER_ERROR,
            description = FAILED_RESPONSE,
            body = ErrorResponse,
            example = json!(ErrorResponse::default())
        ),
    )
)]
pub async fn ai_endpoint(
    req: &mut Request,
    res: &mut Response,
    data: JsonBody<SearchWithAiBody>,
) -> Json<EndpointResponse<RecipeCardList>> {
    let uri = req.uri().path();
    let parts: Vec<&str> = uri.split('/').collect();
    let new_url = parts[2..].join("/");
    let url: String = format!("{SERVICE}/{new_url}");

    return match get_response::<&str, SearchWithAiBody, RecipeCardList>(
        Method::POST,
        url,
        None,
        Some(data.into_inner()),
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
