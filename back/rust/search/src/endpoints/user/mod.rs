use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

pub mod search_users;

#[derive(Serialize, Deserialize, ToSchema, Debug)]
pub struct SearchUsersPayload {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub query: Option<String>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub sort: Option<String>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub order: Option<String>,

    pub start: u32,
    pub count: u32,
}

impl SearchUsersPayload {
    pub fn into_params(self) -> SearchUsersParams {
        SearchUsersParams {
            query: self.query.unwrap_or("".to_string()),
            sort: self.sort.unwrap_or("_id".to_string()),
            order: if self.order.unwrap_or("asc".to_string()).eq("asc") {
                1
            } else {
                -1
            },
            start: self.start,
            count: self.count,
        }
    }
}

pub struct SearchUsersParams {
    pub query: String,
    pub sort: String,
    pub order: i32,
    pub start: u32,
    pub count: u32,
}

