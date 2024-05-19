use crate::config::Configuration;
use anyhow::Context;

pub mod rating;

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
