use crate::repository::cooking_app::CookingAppRepository;
use anyhow::Result;
use once_cell::sync::OnceCell;

pub const MONGO_URI: &str = "MONGO_URI";
pub const AI_API_URL: &str = "AI_API_URL";
pub const HOST: &str = "HOST";
pub const PORT: &str = "PORT";

#[derive(Debug)]
pub struct EnvironmentVariables {
    pub mongo_uri: String,
    pub ai_api_url: String,
    pub host: String,
    pub port: u32,
}

impl EnvironmentVariables {
    pub fn get_env() -> Self {
        Self {
            mongo_uri: std::env::var(MONGO_URI).unwrap_or("mongodb://localhost:27017/?directConnection=true".into()),
            ai_api_url: std::env::var(AI_API_URL).unwrap_or("http://localhost:8912".into()),
            host: std::env::var(HOST).unwrap_or("0.0.0.0".into()),
            port: std::env::var(PORT).unwrap_or("3000".into()).parse::<u32>().unwrap_or(3000),
        }
    }
}

pub struct CookingAppContext {
    pub repository: CookingAppRepository,
    pub env: EnvironmentVariables,
}

pub static CONTEXT: OnceCell<CookingAppContext> = OnceCell::new();

#[inline]
pub fn get_global_context() -> Result<&'static CookingAppContext> {
    CONTEXT.get().map_or_else(
        || Err(anyhow::Error::msg("Couldn't load CookingApp Context")),
        Ok,
    )
}

#[macro_export]
macro_rules! get_endpoint_context {
    ($res:expr) => {
        match get_global_context() {
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
