use bson::oid::ObjectId;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use super::{expiring_token::ExpiringToken, user_login_data_external::UserLoginDataExternal, users_login_data::UserLoginData};

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
    pub login: Option<UserLoginData>,
    pub external_login: Option<UserLoginDataExternal>,
    pub message_history: Vec<String>,
    pub search_history: Vec<String>,
    pub saved_recipes: Vec<ObjectId>,
    pub ratings: Vec<ObjectId>,
    pub allergens: Vec<String>,
    pub sessions: Vec<ExpiringToken>,
}

impl User {
    #[must_use]
    pub const fn get_collection_name() -> &'static str {
        "user"
    }
}
