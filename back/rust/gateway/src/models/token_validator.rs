use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct Success {
    pub user_id: String,
    pub user_roles: u32,
    pub token_type: String,
}