
use super::{EndpointResponse, SERVICE};
use crate::{
    get_redirect_url,
    endpoints::{
        redirect,
        rating::common::{body_rating_response, PutPatchType, HEADER_KEYS}
    },
    config::get_global_context,
    models::{
        ErrorResponse,
        rating::RatingUpdate
    }
};
use salvo::{
    oapi::{
        endpoint,
        extract::JsonBody
    },
    prelude::Json,
    Request, Response, Writer
};
use reqwest::{Method, StatusCode};
use tracing::error;


#[endpoint(
    parameters(
        ("rating_id" = String, description = "Rating id")
    )
)]
pub async fn patch_rating_endpoint(
    rating_update: JsonBody<RatingUpdate>,
    req: &mut Request,
    res: &mut Response,
) -> Json<EndpointResponse> {
    let url: String = get_redirect_url!(req, res, SERVICE);
    return match body_rating_response::<[(&str, &str); 0]>(
        Method::PATCH,
        url.as_str(),
        &[],
        PutPatchType::RatingUpdate(rating_update.into_inner()),
        &headers,
    )
        .await
    {
        Ok(response) => Json(response),
        Err(_) => {
            res.status_code(StatusCode::BAD_REQUEST);
            Json(EndpointResponse::Error(ErrorResponse::default()))
        }
    };
}
