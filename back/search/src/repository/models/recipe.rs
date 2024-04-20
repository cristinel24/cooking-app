use bson::oid::ObjectId;
use salvo::prelude::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, ToSchema, Debug, Default)]
#[serde(rename_all = "camelCase")]
pub struct ResponseRecipe {
    pub author: Author,
    pub title: String,
    pub description: String,
    pub prep_time: u32,
    pub allergens: Vec<Option<String>>,
    pub tags: Vec<Option<String>>,
}

#[derive(Serialize, Deserialize, ToSchema, Debug, Default)]
#[serde(rename_all = "camelCase")]
pub struct Author {
    pub icon: String,
    pub username: String,
    pub display_name: String,
    pub roles: i32,
}

impl From<Recipe> for ResponseRecipe {
    fn from(value: Recipe) -> Self {
        Self {
            author: value.author,
            title: value.title,
            description: value.description,
            prep_time: value.prep_time,
            allergens: value.allergens,
            tags: value.tags,
        }
    }
}

#[derive(Serialize, Deserialize, Debug)]
#[serde(rename_all = "camelCase")]
pub struct Recipe {
    pub author: Author,
    pub title: String,
    pub description: String,
    pub prep_time: u32,
    pub allergens: Vec<Option<String>>,
    pub tags: Vec<Option<String>>,
}

impl Recipe {
    #[must_use]
    pub const fn get_collection_name() -> &'static str {
        "recipe"
    }
}
