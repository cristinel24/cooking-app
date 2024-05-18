use crate::{
    get_redirect_url,
    models::ErrorResponse,
    config::get_global_context,
    endpoints::{
        redirect,
        rating::{
            EndpointResponse,
            common::{body_rating_response, PutPatchType, HEADER_KEYS},
            SERVICE
        }
    }
};
use salvo::{
    oapi::endpoint,
    http::StatusCode,
    prelude::Json,
    Request, Response
};
use reqwest::Method;
use tracing::error;

#[endpoint(
    parameters(
        ("rating_id" = String, description = "Rating id")
    )
)]
pub async fn delete_rating_endpoint(
    req: &mut Request,
    res: &mut Response,
) -> Json<EndpointResponse> {
    let url: String = get_redirect_url!(req, res, SERVICE);
    let rating_id = req.param::<String>("rating_id").unwrap_or_default();

    return match body_rating_response(
        Method::DELETE,
        url.as_str(),
        &[("rating_id", rating_id)],
        PutPatchType::None,
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
