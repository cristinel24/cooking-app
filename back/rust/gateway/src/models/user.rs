use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct User {
    pub id: String,
    pub username: String,
    pub display_name: String,
    pub icon: String,
    pub roles: u32,
    pub rating_avg: f32,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct CardData {
    pub id: String,
    pub username: String,
    pub display_name: String,
    pub icon: String,
    pub roles: u32,
    pub rating_avg: f32,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct FullData {
    pub id: String,
    pub username: String,
    pub display_name: String,
    pub icon: String,
    pub roles: u32,
    pub rating_avg: f32,
    pub description: String,
    pub recipes: Vec<String>,
    pub ratings: Vec<String>,
    pub email: String,
    pub follows_count: u32,
    pub followers_count: u32,
    pub allergens: Vec<String>,
    pub search_history: Vec<String>,
    pub message_history: Vec<String>,
    pub saved_recipes: Vec<String>,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct CardsRequestData {
    pub ids: Vec<String>,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct Cards {
    pub cards: Vec<CardData>,
}
