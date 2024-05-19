use crate::models::user::User;
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct DataCard {
    pub parent_id: String,
    pub parent_type: String,
    pub author: User,
    pub updated_at: String,
    pub rating: usize,
    pub description: String,
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
    pub author_id: String,
    pub description: String,
    pub rating: usize,
    pub parent_type: String,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct Update {
    pub description: String,
    pub rating: usize,
}
