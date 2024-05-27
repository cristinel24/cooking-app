use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct SignInBody {
    pub username: String,
    pub email: String,
    pub password: String,
    pub display_name: Option<String>,
}
