use chrono::{DateTime, Utc};
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, ToSchema, Debug)]
#[serde(rename_all = "camelCase")]
pub struct User {
    pub username: String,
    pub sum_rating: i32,
}

impl User {
    #[must_use]
    pub const fn get_collection_name() -> &'static str {
        "user"
    }
}
