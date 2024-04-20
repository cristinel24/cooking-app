use crate::repository::models::recipe::{Recipe, ResponseRecipe};
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize, Serializer};

pub mod search_ai_tokens;

#[derive(Serialize, Deserialize, ToSchema)]
pub struct AiTokensPayload {
    pub tokens: Vec<String>,
}

#[derive(Deserialize, ToSchema)]
pub enum RecipeResponse {
    Success(RecipeResponsePayload),
    Error(ErrorResponse),
}

impl Default for RecipeResponse {
    fn default() -> Self {
        Self::Success(RecipeResponsePayload::default())
    }
}

impl Serialize for RecipeResponse {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        match self {
            Self::Success(ok_response) => ok_response.serialize(serializer),
            Self::Error(err) => err.serialize(serializer),
        }
    }
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
pub struct RecipeResponsePayload {
    pub data: Vec<ResponseRecipe>,
    pub count: u32,
}

#[derive(Serialize, Deserialize, ToSchema)]
pub struct ErrorResponse {
    pub message: String,
}
