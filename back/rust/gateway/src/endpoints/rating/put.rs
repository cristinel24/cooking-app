use super::{EndpointResponse, SERVICE};
use crate::{
    config::get_global_context,
    endpoints::{
        rating::common::{body_rating_response, PutPatchType},
        redirect,
    },
    get_redirect_url,
    models::{rating::Create, ErrorResponse},
};
use reqwest::{Method, StatusCode};
use salvo::{
    oapi::{endpoint, extract::JsonBody},
    prelude::Json,
    Request, Response, Writer,
};
use tracing::error;

#[endpoint(
    parameters(
        ("parent_id" = String, description = "Rating id")
    )
)]
pub async fn put_rating_endpoint(
    rating_create: JsonBody<Create>,
    req: &mut Request,
    res: &mut Response,
) -> Json<EndpointResponse> {
    println!("{:#?}", req.uri());
    let url: String = get_redirect_url!(req, res, SERVICE);
    let parent_id = req.param::<String>("parent_id").unwrap_or_default();

    return (body_rating_response(
        Method::PUT,
        url.as_str(),
        &[("parent_id", parent_id)],
        PutPatchType::RatingCreate(rating_create.into_inner()),
        req.headers().clone(),
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
