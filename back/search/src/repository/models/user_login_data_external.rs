use serde::{Deserialize, Serialize};

use super::external_provider::ExternalProvider;

#[derive(Serialize, Deserialize, Debug)]
#[serde(rename_all = "camelCase")]
pub struct UserLoginDataExternal {
    pub provider_token: String,
    pub provider_data: ExternalProvider,
}

impl UserLoginDataExternal {
    #[must_use]
    pub const fn get_collection_name() -> &'static str {
        "user_login_data_external"
    }
}
