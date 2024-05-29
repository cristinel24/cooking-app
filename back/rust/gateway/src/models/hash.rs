use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct Primary {
    pub hash_algorithm_name: String,
    pub hash: String,
    pub salt: String,
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
#[serde(rename_all = "camelCase")]
pub struct AlgorithmName {
    pub hash: String,
    pub salt: String,
}
