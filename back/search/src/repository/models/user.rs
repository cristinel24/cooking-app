use salvo::prelude::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, ToSchema, Debug)]
#[serde(rename_all = "camelCase")]
pub struct User {
    pub icon: String,
    pub display_name: String,
    pub username: String,
    pub roles: i32,
    pub rating_ratio: f32,
}

#[derive(Serialize, Deserialize, ToSchema, Default, Debug)]
pub struct UserAggregation {
    pub data: Vec<User>,
    pub count: u32,
}

impl User {
    #[must_use]
    pub const fn get_collection_name() -> &'static str {
        "user"
    }
}
