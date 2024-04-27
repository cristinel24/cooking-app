use crate::repository::models::user::Author;
use salvo::prelude::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, ToSchema, Debug, Default)]
#[serde(rename_all = "camelCase")]
pub struct Recipe {
    pub author: Author,
    pub title: String,
    pub description: String,
    pub prep_time: u32,
    pub allergens: Vec<String>,
    pub tags: Vec<String>,
}

impl Recipe {
    #[must_use]
    pub const fn get_collection_name() -> &'static str {
        "recipe"
    }
}
