use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};
use crate::models::user::CardData;

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct FollowCount {
    pub followers_count: u32
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct Follow {
    pub followers: Vec<CardData>
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct Follows {
    pub follows_id: String
}