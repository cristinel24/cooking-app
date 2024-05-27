use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct RoleChange {
    pub verified: Option<i32>,
    pub admin: Option<i32>,
    pub premium: Option<i32>,
    pub banned: Option<i32>,
}
