use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct RegisterBody {
    pub username: String,
    pub email: String,
    pub password: String,
    pub display_name: Option<String>,
}
