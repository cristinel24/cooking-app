
use super::{SERVICE, EndpointResponse};
use crate::{
    get_redirect_url,
    endpoints::{
        redirect,
        rating::common::{body_rating_response, PutPatchType, HEADER_KEYS}
    },
    config::get_global_context,
    models::{
        ErrorResponse,
        rating::RatingCreate
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
        ("parent_id" = String, description = "Rating id")
    )
)]
pub async fn put_rating_endpoint(
    rating_create: JsonBody<RatingCreate>,
    req: &mut Request,
    res: &mut Response,
) -> Json<EndpointResponse> {
    println!("{:#?}", req.uri());
    let url: String = get_redirect_url!(req, res, SERVICE);
    let parent_id = req.param::<String>("parent_id").unwrap_or_default();

    return match body_rating_response(
        Method::PUT,
        url.as_str(),
        &[("parent_id", parent_id)],
        PutPatchType::RatingCreate(rating_create.into_inner()),
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
