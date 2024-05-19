mod common;
pub mod delete;

pub use delete::delete_rating_endpoint;
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize, Serializer};
pub mod get;
pub use get::get_rating_endpoint;
pub mod patch;
pub use patch::patch_rating_endpoint;
pub mod put;
use crate::models::rating::List;
use crate::models::ErrorResponse;
pub use put::put_rating_endpoint;

pub const SERVICE: &str = "rating";

#[derive(Deserialize, ToSchema)]
pub enum EndpointResponse {
    RatingList(List),
    Ok(String),
    Error(ErrorResponse),
}

impl Serialize for EndpointResponse {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        match self {
            Self::RatingList(ok_response) => ok_response.serialize(serializer),
            Self::Ok(ok_response) => ok_response.serialize(serializer),
            Self::Error(err) => err.serialize(serializer),
        }
    }
}
