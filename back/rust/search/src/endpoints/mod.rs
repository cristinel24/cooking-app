use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize, Serializer};

pub mod ai;
pub mod common;
pub mod recipe;
pub mod user;

pub const INTERNAL_SERVER_ERROR: &str = "Internal Server Error!";

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

#[derive(Serialize, Deserialize, Debug, ToSchema)]
pub struct ErrorResponse {
    pub message: String,
}

impl Default for ErrorResponse {
    fn default() -> Self {
        Self {
            message: "Error".to_string(),
        }
    }
}
