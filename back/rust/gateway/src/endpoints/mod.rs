use crate::config::Configuration;
use crate::models::ErrorResponse;
use anyhow::Context;
use reqwest::header::HeaderMap;
use reqwest::{Client, Method, Response};
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize, Serializer};

pub mod ai;
pub mod allergen;
pub mod email;
pub mod follow_manager;
pub mod history_manager;
pub mod message_history_manager;
pub mod profile_data_changer;
pub mod rating;
pub mod recipe_creator;
pub mod recipe_retriever;
pub mod recipe_saver;
pub mod role_changer;
pub mod tag;
pub mod user_destroyer;
pub mod user_retriever;
pub mod image_storage;

const SUCCESSFUL_RESPONSE: &str = "Successful operation response";
const FAILED_RESPONSE: &str = "Failed operation response";

#[derive(Deserialize, ToSchema)]
pub(crate) enum EndpointResponse<T: Serialize> {
    Ok(T),
    Null(String),
    Error(ErrorResponse),
}

impl<T: Serialize> Default for EndpointResponse<T> {
    fn default() -> Self {
        Self::Error(ErrorResponse::default())
    }
}

impl<T: Serialize> Serialize for EndpointResponse<T> {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        match self {
            Self::Ok(ok_response) => ok_response.serialize(serializer),
            Self::Null(ok_response) => ok_response.serialize(serializer),
            Self::Error(err) => err.serialize(serializer),
        }
    }
}

/// # Errors
/// * Couldn't build `reqwest` client
pub(crate) async fn get_response<
    T: Serialize + ?Sized + Send + Sync,
    H: Serialize + Send + Sync,
    G: Serialize + for<'de> Deserialize<'de>,
>(
    method: Method,
    service_url: String,
    params: Option<&T>,
    json_body: Option<H>,
    headers: Option<HeaderMap>,
    is_null: bool,
) -> anyhow::Result<EndpointResponse<G>> {
    let mut req_builder = Client::new().request(method, service_url);
    if let Some(params) = params {
        req_builder = req_builder.query(params);
    }

    if let Some(json_body) = json_body {
        req_builder = req_builder.json(&json_body);
    }

    if let Some(headers) = headers {
        req_builder = req_builder.headers(headers);
    }

    let response: Response = req_builder.send().await?;

    if response.status().is_success() {
        if is_null {
            Ok(EndpointResponse::Null(response.text().await?))
        } else {
            Ok(EndpointResponse::Ok(response.json::<G>().await?))
        }
    } else {
        Ok(EndpointResponse::Error(
            response.json::<ErrorResponse>().await?,
        ))
    }
}

/// # Errors
/// * Couldn't get `service`
pub fn redirect(context: &Configuration, url: &str, service: &str) -> anyhow::Result<String> {
    let service = context
        .services
        .get(service)
        .context("Cannot get service")?;
    Ok(format!("{}:{}/{}", service.url, service.port, url))
}

#[macro_export]
macro_rules! get_redirect_url {
    ($req:expr, $res:expr, $uri:expr, $service:expr) => {{
        let context = match get_global_context() {
            Ok(value) => value,
            Err(e) => {
                error!("Error: {e}");
                $res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
                return Json(EndpointResponse::Error(ErrorResponse::default()));
            }
        };
        match redirect(context, $uri, $service) {
            Ok(value) => value,
            Err(_) => {
                $res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
                return Json(EndpointResponse::Error(ErrorResponse::default()));
            }
        }
    }};
}
