use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

use super::user;

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct Body {
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
    pub author: Card,
    pub title: String,
    pub description: String,
    pub prep_time: u32,
    pub steps: Vec<String>,
    pub ingredients: Vec<String>,
    pub allergens: Vec<String>,
    pub tags: Vec<String>,
    pub thumbnail: String,
    pub view_count: u32,
    pub user_rating: Option<Card>,
    pub is_favorite: Option<bool>,
    pub rating_avg: f32,
    pub created_at: String,
    pub updated_at: String,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct Card {
    pub id: String,
    pub author: user::Card,
    pub title: String,
    pub description: String,
    pub prep_time: u32,
    pub allergens: Vec<String>,
    pub tags: Vec<String>,
    pub thumbnail: String,
    pub view_count: u32,
    pub is_favorite: Option<bool>,
    pub rating_avg: f32,
    pub created_at: String,
    pub updated_at: String,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct CardList {
    pub total: u32,
    pub data: Vec<Card>,
}
