use reqwest::header::{HeaderMap, HeaderName, HeaderValue};
use reqwest::{Client, Method};
use serde::Serialize;
use tracing::warn;
use crate::{
    endpoints::rating::EndpointResponse,
    models::{
        ErrorResponse,
        rating::{RatingCreate, RatingUpdate}
    }
};

pub enum PutPatchType {
    RatingCreate(RatingCreate),
    RatingUpdate(RatingUpdate),
    None
}

pub async fn body_rating_response<T: Serialize + ?Sized>(
    method: Method,
    service_url: &str,
    params: &T,
    json_body: PutPatchType,
    headers: HeaderMap,
) -> anyhow::Result<EndpointResponse> {
    let mut req_builder = Client::new()
        .request(method, service_url)
        .query(params)
        .headers(headers);

    req_builder = match json_body {
        PutPatchType::RatingCreate(value) => req_builder.json(&value),
        PutPatchType::RatingUpdate(value) => req_builder.json(&value),
        PutPatchType::None => req_builder
    };

    let response = req_builder.send().await?;

    if response.status().is_success() {
        Ok(EndpointResponse::Ok(response.text().await?))
    } else {
        Ok(EndpointResponse::Error(
            response.json::<ErrorResponse>().await?,
        ))
    }
}

