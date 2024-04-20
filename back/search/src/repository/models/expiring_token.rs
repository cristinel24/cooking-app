use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
#[serde(rename_all = "camelCase")]
pub struct ExpiringToken {
    pub value: String,
    #[serde(with = "bson::serde_helpers::chrono_datetime_as_bson_datetime")]
    pub date: DateTime<Utc>,
}

impl ExpiringToken {
    #[must_use]
    pub const fn get_collection_name() -> &'static str {
        "expiring_token"
    }
}
