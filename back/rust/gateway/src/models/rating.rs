use crate::models::user::User;
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct RatingDataCard {
    pub parent_id: String,
    pub parent_type: String,
    pub author: User,
    pub updated_at: String,
    pub rating: usize,
    pub description: String,
}

#[derive(Serialize, Deserialize, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct RatingList {
    pub ratings: Vec<RatingDataCard>,
    pub total: usize,
}

#[derive(Serialize, Deserialize, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct RatingCreate {
    pub author_id: String,
    pub description: String,
    pub rating: usize,
    pub parent_type: String,
}

#[derive(Serialize, Deserialize, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct RatingUpdate {
    pub description: String,
    pub rating: usize,
}
