use crate::models::ErrorResponse;
use reqwest::header::HeaderMap;
use reqwest::{Client, Method, Response};
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize, Serializer};
use tracing::debug;

pub mod ai;
pub mod allergen_manager;
pub mod credentials_change_requester;
pub mod email_changer;
pub mod follow_manager;
pub mod image_storage;
pub mod login;
pub mod message_history_manager;
pub mod password_changer;
pub mod profile_data_changer;
pub mod rating;
pub mod recipe_creator;
pub mod recipe_editor;
pub mod recipe_retriever;
pub mod recipe_saver;
pub mod register;
pub mod role_changer;
pub mod search;
pub mod search_history_manager;
pub mod tag_manager;
pub mod user_destroyer;
pub mod user_retriever;
pub mod username_changer;
pub mod verifier;

const SUCCESSFUL_RESPONSE: &str = "Successful operation response";
const FAILED_RESPONSE: &str = "Failed operation response";

#[derive(Deserialize, ToSchema, Debug)]
pub(crate) enum EndpointResponse<T: Serialize> {
    Ok(T),
    Null(String),
    Error((ErrorResponse, u16)),

    ServerError(ErrorResponse),
}

impl<T: Serialize> Default for EndpointResponse<T> {
    fn default() -> Self {
        Self::ServerError(ErrorResponse::default())
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
            Self::ServerError(err) => err.serialize(serializer),
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
    debug!("{method:?} {service_url}");
    let mut req_builder = Client::new().request(method, format!("http://{service_url}"));
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
    let code = response.status().as_u16();

    if response.status().is_success() {
        if is_null {
            Ok(EndpointResponse::Null(response.text().await?))
        } else {
            Ok(EndpointResponse::Ok(response.json::<G>().await?))
        }
    } else {
        Ok(EndpointResponse::Error(
            (response.json::<ErrorResponse>().await?, code),
        ))
    }
}
