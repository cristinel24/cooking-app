use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize, Serializer};
use crate::repository::models::recipe::Recipe;

pub mod recipe;
pub mod test;
pub mod search_general;

pub const INTERNAL_SERVER_ERROR: &str = "Internal Server Error!";


#[derive(Serialize, Deserialize, ToSchema)]
pub struct InputPayload {
    pub data: String,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub filters: Option<Filters>,

    pub page: u32,
    pub results_per_page: u32,
}


#[derive(Serialize, Deserialize, ToSchema)]
pub struct Filters {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub ingredients: Option<Vec<String>>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub blacklist: Option<BlacklistedFilters>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub tags: Option<Vec<String>>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub authors: Option<Vec<String>>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub prep_time: Option<u32>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub rating: Option<u32>,
}

#[derive(Serialize, Deserialize, ToSchema)]
pub struct BlacklistedFilters {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub ingredients: Option<Vec<String>>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub tags: Option<Vec<String>>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub allergens: Option<Vec<String>>,
}

#[derive(Serialize, Deserialize, ToSchema)]
pub struct SearchResponse {
    pub recipes: AggregationResponse,
    pub users: AggregationResponse,
}

#[derive(Deserialize, ToSchema)]
pub enum EndpointResponse {
    Success(AggregationResponse),
    SuccessSearch(SearchResponse),
    Error(ErrorResponse),
}

impl Default for EndpointResponse {
    fn default() -> Self {
        Self::Success(AggregationResponse::default())
    }
}

impl Serialize for EndpointResponse {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        match self {
            Self::Success(ok_response) => ok_response.serialize(serializer),
            Self::SuccessSearch(ok_response) => ok_response.serialize(serializer),
            Self::Error(err) => err.serialize(serializer),
        }
    }
}

#[derive(Serialize, Deserialize, Default, ToSchema)]
pub struct AggregationResponse {
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
            message: "Error".to_string(),
        }
    }
}
