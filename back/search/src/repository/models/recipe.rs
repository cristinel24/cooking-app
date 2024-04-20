use bson::Bson;
use bson::oid::ObjectId;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Recipe {
    #[serde(with = "bson::serde_helpers::chrono_datetime_as_bson_datetime")]
    pub updated_at: DateTime<Utc>,
    pub author_id: ObjectId,
    pub title: String,
    pub sum_rating: u32,
    pub count_rating: u32,
    pub description: String,
    pub prep_time: u32,
    pub steps: Vec<String>,
    pub ingredients: Vec<String>,
    pub allergens: Vec<String>,
    pub tags: Vec<String>,
    pub tokens: Vec<String>,
    pub ratings: Vec<ObjectId>,
}

impl Recipe {
    #[must_use]
    pub const fn get_collection_name() -> &'static str {
        "report"
    }
}
