use crate::repository::service::CollectionName;
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct User {
    pub id: String,
    pub username: String,
    pub display_name: String,
    pub icon: String,
    pub roles: u32,
    pub rating_avg: f32,
    pub created_at: String,
    pub updated_at: String,
    // TODO: ?
    pub is_following: Option<bool>,
    pub is_followed_by: Option<bool>,
}

impl CollectionName for User {
    fn get_collection_name() -> &'static str {
        "user"
    }
}
