use crate::repository::models::user::{User, UserAggregation};
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize, Serializer};

pub mod search_users;

#[derive(Serialize, Deserialize, ToSchema)]
pub enum UserResponse {
    Success(UserAggregation),
    Error(ErrorResponse),
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
pub struct UserResponsePayload {
    pub data: Vec<User>,
    pub count: u32,
}

#[derive(Serialize, Deserialize, ToSchema)]
pub struct ErrorResponse {
    pub message: String,
}
