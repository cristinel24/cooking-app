use crate::repository::service::CollectionName;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
pub struct ExpiringToken {
    pub value: String,
    pub r#type: String,
}

impl CollectionName for ExpiringToken {
    fn get_collection_name() -> &'static str {
        "expiring_token"
    }
}
