use crate::config::Configuration;
use anyhow::Context;

pub mod rating;


const SUCCESSFUL_RESPONSE: &str = "Successful operation response";
const FAILED_RESPONSE: &str = "Failed operation response";
const INTERNAL_SERVER_ERROR: &str = "Internal Server Error";


/// # Errors
/// * Couldn't get `service`
pub fn redirect(context: &Configuration, url: &str, service: &str) -> anyhow::Result<String> {
    let service = context
        .services
        .get(service)
        .context("Cannot get service")?;
    Ok(format!("{}:{}{}", service.url, service.port, url))
}

#[macro_export]
macro_rules! get_redirect_url {
    ($req:expr, $res:expr, $service:expr) => {{
        let context = match get_global_context() {
            Ok(value) => value,
            Err(e) => {
                error!("Error: {e}");
                $res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
                return Json(EndpointResponse::Error(ErrorResponse::default()));
            }
        };
        match redirect(context, $req.uri().path(), $service) {
            Ok(value) => value,
            Err(_) => {
                $res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
                return Json(EndpointResponse::Error(ErrorResponse::default()));
            }
        }
    }};
}
