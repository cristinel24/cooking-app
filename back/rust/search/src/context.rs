use crate::repository::cooking_app::CookingAppRepository;
use anyhow::Result;
use once_cell::sync::OnceCell;

pub const MONGO_URI_VAR: &str = "MONGO_SERVER";
pub const AI_SERVER_VAR: &str = "AI_SERVER";
pub const AUTH_SERVER_VAR: &str = "AUTH_SERVER";
pub const SERVER: &str = "SERVER";
pub const PORT: &str = "PORT";

pub struct EnvironmentVariables {
    pub mongo_server: String,
    pub ai_server: String,
    pub auth_server: String,
    pub server: String,
    pub port: u32,
}

impl Default for EnvironmentVariables {
    fn default() -> Self {
        Self {
            mongo_server: "mongodb://localhost:27017".to_owned(),
            ai_server: "http://127.0.0.1:8000".to_owned(),
            auth_server: "http://localhost:8082".to_owned(),
            server: "0.0.0.0".to_owned(),
            port: 3000,
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
