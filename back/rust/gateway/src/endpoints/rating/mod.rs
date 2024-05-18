mod common;
pub mod delete_rating;

use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize, Serializer};
pub use delete_rating::delete_rating_endpoint;
pub mod get_rating;
pub use get_rating::get_rating_endpoint;
pub mod patch_rating;
pub use patch_rating::patch_rating_endpoint;
pub mod put_rating;
pub use put_rating::put_rating_endpoint;
use crate::models::ErrorResponse;
use crate::models::rating::RatingList;

pub const SERVICE: &str = "rating";


#[derive(Deserialize, ToSchema)]
pub enum EndpointResponse {
    RatingList(RatingList),
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