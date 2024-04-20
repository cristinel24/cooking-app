use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize, Serializer};

pub mod recipe;
pub mod test;

pub const INTERNAL_SERVER_ERROR: &str = "Internal Server Error!";

#[derive(Deserialize, ToSchema)]
pub enum EndpointResponse {
    Success(OkResponse),
    Error(ErrorResponse),
}

impl Default for EndpointResponse {
    fn default() -> Self {
        Self::Success(OkResponse::default())
    }
}

impl Serialize for EndpointResponse {
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
pub struct OkResponse {
    pub data: Vec<String>,
}

#[derive(Serialize, Deserialize, ToSchema)]
pub struct ErrorResponse {
    pub message: String,
}
