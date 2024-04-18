use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize, Serializer};

pub mod test;

#[derive(Deserialize, ToSchema)]
pub enum EndpointResponse {
    Success(OkResponse),
    Error(ErrorResponse),
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

#[derive(Serialize, Deserialize, ToSchema)]
pub struct OkResponse {
    pub data: Vec<String>,
}

#[derive(Serialize, Deserialize, ToSchema)]
pub struct ErrorResponse {
    pub message: String,
}
