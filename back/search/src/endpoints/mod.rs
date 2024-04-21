use crate::repository::models::recipe::Recipe;
use crate::repository::models::user::User;
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize, Serializer};

pub mod recipe;
pub mod search_general;
pub mod user;

pub const INTERNAL_SERVER_ERROR: &str = "Internal Server Error!";

#[macro_export]
macro_rules! get_context {
    ($res:expr) => {
        match get_context() {
            Ok(value) => value,
            Err(e) => {
                error!("Error: {e}");
                $res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
                return Json(EndpointResponse::Error(ErrorResponse {
                    message: e.to_string(),
                }));
            }
        }
    };
}

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

#[derive(Serialize, Deserialize, Default, ToSchema)]
pub struct SearchResponse {
    pub recipes: AggregationResponse<Recipe>,
    pub users: AggregationResponse<User>,
}

#[derive(Deserialize, ToSchema)]
pub enum EndpointResponse<T: Serialize> {
    SuccessSearch(SearchResponse),

    Success(AggregationResponse<T>),
    Error(ErrorResponse),
}

impl<T: Serialize> Default for EndpointResponse<T> {
    fn default() -> Self {
        Self::SuccessSearch(SearchResponse::default())
    }
}

impl<T: Serialize> Serialize for EndpointResponse<T> {
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
pub struct AggregationResponse<T: Serialize> {
    pub count: u32,
    pub data: Vec<T>,
}

#[derive(Serialize, Deserialize, Debug, ToSchema)]
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
