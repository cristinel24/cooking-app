use crate::repository::{models::user::User, service::CollectionName};
use salvo::prelude::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, ToSchema, Debug, Default)]
#[serde(rename_all = "camelCase")]
pub struct Recipe {
    pub id: String,
    pub author: User,
    pub title: String,
    pub rating_avg: f32,
    pub description: String,
    pub prep_time: u32,
    pub allergens: Vec<String>,
    pub tags: Vec<String>,
    pub thumbnail: String,
    pub view_count: u32,
    pub created_at: String,
    pub updated_at: String,
}

impl CollectionName for Recipe {
    fn get_collection_name() -> &'static str {
        "recipe"
    }
}
