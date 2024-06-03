use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

use super::user::Card;

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct Rating {
    pub id: String,
    pub parent_id: String,
    pub parent_type: String,
    pub author: Card,
    pub updated_at: String,
    pub created_at: String,
    pub rating: usize,
    pub description: String,
    pub children_count: usize,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct List {
    pub data: Vec<Rating>,
    pub total: usize,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct CreateBody {
    pub description: String,
    pub rating: usize,
    pub parent_type: String,
    pub parent_id: String,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct UpdateBody {
    pub description: String,
    pub rating: usize,
}
