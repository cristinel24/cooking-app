use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

pub mod search_ai_tokens;
pub mod search_fuzzy_title;

#[derive(Serialize, Deserialize, ToSchema)]
pub struct AiTokensPayload {
    pub tokens: Vec<String>,
}
