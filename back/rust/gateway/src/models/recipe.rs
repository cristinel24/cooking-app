use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct Recipe {
    pub title: String,
    pub description: String,
    pub prep_time: u64,
    pub steps: Vec<String>,
    pub ingredients: Vec<String>,
    pub allergens: Vec<String>,
    pub tags: Vec<String>,
    pub thumbnail: Vec<String>,
}