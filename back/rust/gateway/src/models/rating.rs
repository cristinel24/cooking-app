use crate::models::user::CardData;
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct DataCard {
    pub parent_id: String,
    pub parent_type: String,
    pub author: CardData,
    pub updated_at: String,
    pub created_at: String,
    pub rating: usize,
    pub description: String,
    pub children_count: usize,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct List {
    pub ratings: Vec<DataCard>,
    pub total: usize,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct Create {
    pub description: String,
    pub rating: usize,
    pub parent_type: String,
    pub parent_id: String,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct Update {
    pub description: String,
    pub rating: usize,
}
