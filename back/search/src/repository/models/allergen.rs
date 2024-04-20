use salvo::prelude::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, ToSchema, Debug, Default)]
#[serde(rename_all = "camelCase")]
pub struct Allergen {
    pub allergen: String,
    pub counter: u32,
}

impl Allergen {
    #[must_use]
    pub const fn get_collection_name() -> &'static str {
        "allergen"
    }
}
