use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

use super::common::{Filters, SearchRecipesParams};

pub mod search_ai;

#[derive(Serialize, Deserialize, ToSchema, Debug)]
pub struct SearchAiPayload {
    pub query: String,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub sort: Option<String>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub order: Option<String>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub filters: Option<Filters>,

    pub start: u32,
    pub count: u32,
}

impl SearchAiPayload {
    pub fn to_params(self, tokens: Vec<String>) -> SearchRecipesParams {
        SearchRecipesParams {
            query: self.query,
            sort: self.sort.unwrap_or("_id".to_string()),
            order: if self.order.unwrap_or("asc".to_string()).eq("asc") {
                1
            } else {
                -1
            },
            filters: self.filters,
            start: self.start,
            count: self.count,
            tokens,
        }
    }
}
