use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
#[serde(rename_all = "camelCase")]
pub struct ExternalProvider {
    pub name: String,
    pub endpoint: String,
}

impl ExternalProvider {
    #[must_use]
    pub const fn get_collection_name() -> &'static str {
        "external_provider"
    }
}
