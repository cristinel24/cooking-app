use crate::repository::models::recipe::Recipe;
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize, Serializer};

pub mod search_ai_tokens;
pub mod search_fuzzy_title;

const TOP: u32 = 10u32;


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
    pub count: u32,
    pub data: Vec<Recipe>,
}

#[derive(Serialize, Deserialize, ToSchema)]
pub struct ErrorResponse {
    pub message: String,
}

impl Default for ErrorResponse {
    fn default() -> Self {
        Self {
            message: "Error!".to_string()
        }
    }
}
