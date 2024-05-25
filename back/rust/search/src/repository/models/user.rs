use crate::repository::service::CollectionName;
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct User {
    pub id: String,
    pub icon: String,
    pub display_name: String,
    pub username: String,
    pub roles: i32,
    pub rating_avg: f32,
}

#[derive(Serialize, Deserialize, ToSchema, Default, Debug)]
pub struct UserAggregation {
    pub data: Vec<User>,
    pub count: u32,
}

impl CollectionName for User {
    fn get_collection_name() -> &'static str {
        "user"
    }
}
