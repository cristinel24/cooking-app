use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct RoleChange {
    pub verified: i32,
    pub admin: i32,
    pub premium: i32,
    pub banned: i32,
}