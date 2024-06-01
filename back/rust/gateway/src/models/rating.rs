use crate::models::user::UserCard;
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct RatingCard {
    pub id: String,
    pub parent_id: String,
    pub parent_type: String,
    pub author: UserCard,
    pub updated_at: String,
    pub created_at: String,
    pub rating: usize,
    pub description: String,
    pub children_count: usize,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct RatingList {
    pub data: Vec<RatingCard>,
    pub total: usize,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct RatingCreateBody {
    pub description: String,
    pub rating: usize,
    pub parent_type: String,
    pub parent_id: String,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct RatingUpdateBody {
    pub description: String,
    pub rating: usize,
}
