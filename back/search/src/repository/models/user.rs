use bson::oid::ObjectId;
use chrono::{DateTime, Utc};
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, ToSchema, Debug, Default)]
#[serde(rename_all = "camelCase")]
pub struct Author {
    pub icon: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub username: Option<String>,
    pub display_name: String,
    pub roles: i32,
}

#[derive(Serialize, Deserialize, Debug)]
#[serde(rename_all = "camelCase")]
pub struct User {
    #[serde(with = "bson::serde_helpers::chrono_datetime_as_bson_datetime")]
    pub updated_at: DateTime<Utc>,
    pub icon: String,
    pub display_name: String,
    pub roles: i32,
    pub sum_rating: i32,
    pub count_rating: i32,
    pub description: String,
    pub message_history: Vec<String>,
    pub search_history: Vec<String>,
    pub saved_recipes: Vec<ObjectId>,
    pub ratings: Vec<ObjectId>,
    pub allergens: Vec<String>,
}

impl User {
    #[must_use]
    pub const fn get_collection_name() -> &'static str {
        "user"
    }
}
