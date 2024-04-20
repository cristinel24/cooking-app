use serde::{Deserialize, Serialize};

use super::expiring_token::ExpiringToken;

#[derive(Serialize, Deserialize, Debug)]
#[serde(rename_all = "camelCase")]
pub struct UserLoginData {
    pub username: String,
    pub email: String,
    pub email_status: String,
    pub hash_alg_name: String,
    pub hash: String,
    pub salt: String,
    pub user_change_token: Option<ExpiringToken>,
    pub email_confirm_token: Option<ExpiringToken>,
    pub password_reset_token: Option<ExpiringToken>,
}

impl UserLoginData {
    #[must_use]
    pub const fn get_collection_name() -> &'static str {
        "user_login_data"
    }
}
