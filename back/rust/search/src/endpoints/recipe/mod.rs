use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

use super::common::{Filters, SearchRecipesParams};

pub mod search_ai_tokens;
pub mod search_fuzzy_title;
pub mod search_recipes;

#[derive(Serialize, Deserialize, ToSchema, Debug)]
pub struct SearchRecipesPayload {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub query: Option<String>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub sort: Option<String>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub order: Option<String>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub filters: Option<Filters>,

    pub start: u32,
    pub count: u32,
}

impl SearchRecipesPayload {
    pub fn into_params(self) -> SearchRecipesParams {
        SearchRecipesParams {
            query: self.query.unwrap_or("".to_string()),
            sort: self.sort.unwrap_or("_id".to_string()),
            order: if self.order.unwrap_or("asc".to_string()).eq("asc") {
                1
            } else {
                -1
            },
            filters: self.filters,
            start: self.start,
            count: self.count,
            tokens: Vec::new(),
        }
    }
}

#[derive(Serialize, Deserialize, ToSchema)]
pub struct AiTokensPayload {
    pub tokens: Vec<String>,
}
