use super::{EndpointResponse, SERVICE};
use crate::{
    config::get_global_context,
    endpoints::{
        rating::common::{body_rating_response, PutPatchType},
        redirect,
    },
    get_redirect_url,
    models::{rating::Update, ErrorResponse},
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
        ("rating_id" = String, description = "Rating id")
    )
)]
pub async fn patch_rating_endpoint(
    rating_update: JsonBody<Update>,
    req: &mut Request,
    res: &mut Response,
) -> Json<EndpointResponse> {
    let url: String = get_redirect_url!(req, res, SERVICE);
    return (body_rating_response::<[(&str, &str); 0]>(
        Method::PATCH,
        url.as_str(),
        &[],
        PutPatchType::RatingUpdate(rating_update.into_inner()),
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
