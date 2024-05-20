use salvo::http::StatusCode;
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

pub mod allergens;
pub mod email;
pub mod hash;
pub mod rating;
pub mod role_changer;
pub mod search;
pub mod tags;
pub mod user;

#[derive(Serialize, Deserialize, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct ErrorResponse {
    pub error_code: u32,
}

impl Default for ErrorResponse {
    fn default() -> Self {
        Self {
            error_code: u32::from(StatusCode::INTERNAL_SERVER_ERROR.as_u16()),
        }
    }
}
