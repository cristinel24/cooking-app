use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize, Serializer};

pub mod ai;
pub mod common;
pub mod recipe;
pub mod user;

#[derive(Deserialize, ToSchema)]
pub enum EndpointResponse<T: Serialize> {
    Success(AggregationResponse<T>),
    Error(ErrorResponse),
}

impl<T: Serialize> Serialize for EndpointResponse<T> {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        match self {
            Self::Success(ok_response) => ok_response.serialize(serializer),
            Self::Error(err) => err.serialize(serializer),
        }
    }
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
pub struct AggregationResponse<T: Serialize> {
    pub count: u32,
    pub data: Vec<T>,
}

#[repr(u32)]
pub enum ErrorCodes {
    DbError = 5300,
    AiUnresponsive = 5301,
    Unauthorized = 5302,
    BadData = 5303,
    Unknown = 5304,
}

#[derive(Serialize, Deserialize, Debug, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct ErrorResponse {
    pub error_code: u32,
}

impl Default for ErrorResponse {
    fn default() -> Self {
        Self {
            error_code: ErrorCodes::Unknown as u32,
        }
    }
}
