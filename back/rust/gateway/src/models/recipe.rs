use crate::models::user::UserCard;
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct RecipeBody {
    pub title: String,
    pub description: String,
    pub prep_time: u64,
    pub steps: Vec<String>,
    pub ingredients: Vec<String>,
    pub allergens: Vec<String>,
    pub tags: Vec<String>,
    pub thumbnail: String,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct Recipe {
    pub id: String,
    pub author: UserCard,
    pub title: String,
    pub rating_avg: f32,
    pub description: String,
    pub prep_time: u32,
    pub steps: Vec<String>,
    pub ingredients: Vec<String>,
    pub allergens: Vec<String>,
    pub tags: Vec<String>,
    pub thumbnail: String,
    pub view_count: u32,
    pub created_at: String,
    pub updated_at: String,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct RecipeCard {
    pub id: String,
    pub author: UserCard,
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
