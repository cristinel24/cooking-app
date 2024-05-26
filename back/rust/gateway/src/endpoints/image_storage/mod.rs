use crate::models::ErrorResponse;
use bytes::Bytes;
use reqwest::multipart::{Form, Part};
use reqwest::{Client, Method};
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize, Serializer};

pub mod post;
pub use post::post_image;
pub mod get;
pub use get::get_image;

pub const SERVICE: &str = "image_storage";

#[derive(Deserialize, ToSchema)]
pub enum ImageResponse {
    Bytes(Vec<u8>),
    Null(String),
    Error(ErrorResponse),
}

impl Default for ImageResponse {
    fn default() -> Self {
        Self::Error(ErrorResponse::default())
    }
}

impl Serialize for ImageResponse {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        match self {
            Self::Bytes(ok_response) => ok_response.serialize(serializer),
            Self::Null(ok_response) => ok_response.serialize(serializer),
            Self::Error(err) => err.serialize(serializer),
        }
    }
}

pub(crate) async fn get_put_image(
    method: Method,
    service_url: String,
    payload: Option<Bytes>,
    is_null: bool,
) -> anyhow::Result<ImageResponse> {
    let mut req_builder = Client::new().request(method, service_url);
    if let Some(bytes) = payload {
        req_builder = req_builder.multipart(Form::new().part("file", Part::bytes(bytes.to_vec())));
    }

    println!("{req_builder:#?}");
    let response: reqwest::Response = req_builder.send().await?;

    if response.status().is_success() {
        if is_null {
            Ok(ImageResponse::Null(response.text().await?))
        } else {
            Ok(ImageResponse::Bytes(response.bytes().await?.to_vec()))
        }
    } else {
        Ok(ImageResponse::Error(
            response.json::<ErrorResponse>().await?,
        ))
    }
}
