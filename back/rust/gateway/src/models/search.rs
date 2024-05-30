use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};
use crate::models::recipe::Card;

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct Results {
    pub searches: Vec<String>,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct Query {
    pub search: String,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct AiBody {
    pub query: String,
    pub sort: Option<String>,
    pub order: Option<String>,
    pub filters: Option<Filters>,
    pub start: u32,
    pub count: u32,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct RecipeBody {
    pub query: Option<String>,
    pub sort: Option<String>,
    pub order: Option<String>,
    pub filters: Option<Filters>,
    pub start: u32,
    pub count: u32,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct UserBody {
    pub query: Option<String>,
    pub sort: Option<String>,
    pub order: Option<String>,
    pub start: u32,
    pub count: u32,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct Filters {
    pub ingredients: Option<Vec<String>>,
    pub blacklist: Option<BlacklistedFilters>,
    pub tags: Option<Vec<String>>,
    pub authors: Option<Vec<String>>,
    pub prep_time: Option<u32>,
    pub rating: Option<u32>,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct BlacklistedFilters {
    pub ingredients: Option<Vec<String>>,
    pub tags: Option<Vec<String>>,
    pub allergens: Option<Vec<String>>,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct DataResponse {
    pub count: u32,
    pub data: Vec<Card>,
}