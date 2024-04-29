use crate::repository::service::CollectionName;
use salvo::prelude::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, ToSchema, Debug, Default)]
#[serde(rename_all = "camelCase")]
pub struct Allergen {
    pub allergen: String,
    pub counter: u32,
}

impl CollectionName for Allergen {
    fn get_collection_name() -> &'static str {
        "allergen"
    }
}
