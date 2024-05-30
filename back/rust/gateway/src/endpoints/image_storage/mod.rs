use crate::models::ErrorResponse;
use bytes::Bytes;
use reqwest::multipart::{Form, Part};
use reqwest::{Client, Method};
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize, Serializer};
use std::fs::File;
use std::io::Write;

pub mod post;
pub use post::post_image;
pub mod get;
use crate::models::image_storage::UrlResponse;
pub use get::get_image;

pub const SERVICE: &str = "image_storage";

#[derive(Deserialize, ToSchema)]
pub enum ImageResponse {
    ImageName(String),
    Url(UrlResponse),
    Error((ErrorResponse, u16)),
    ServerError(ErrorResponse),
}

impl Default for ImageResponse {
    fn default() -> Self {
        Self::ServerError(ErrorResponse::default())
    }
}

impl Serialize for ImageResponse {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        match self {
            Self::ImageName(ok_response) => ok_response.serialize(serializer),
            Self::Error(err) => err.serialize(serializer),
            Self::ServerError(err) => err.serialize(serializer),
            Self::Url(url) => url.serialize(serializer),
        }
    }
}

pub(crate) async fn get_post_image(
    method: Method,
    service_url: String,
    payload: Option<Bytes>,
) -> anyhow::Result<ImageResponse> {
    let mut req_builder = Client::new().request(method.clone(), format!("http://{service_url}"));
    if let Some(bytes) = payload {
        req_builder = req_builder
            .multipart(Form::new().part("file", Part::bytes(bytes.to_vec()).file_name("file.png")));
    }

    let response: reqwest::Response = req_builder.send().await?;
    let code = response.status().as_u16();

    if response.status().is_success() {
        if method == Method::POST {
            Ok(ImageResponse::Url(response.json::<UrlResponse>().await?))
        } else {
            let name = service_url.split("/").last().unwrap_or("image");
            let mut file = File::create(format!("{name}.png"))?;
            file.write_all(&*response.bytes().await?.to_vec())?;
            Ok(ImageResponse::ImageName(name.to_string()))
        }
    } else {
        Ok(ImageResponse::Error((
            response.json::<ErrorResponse>().await?,
            code,
        )))
    }
}
