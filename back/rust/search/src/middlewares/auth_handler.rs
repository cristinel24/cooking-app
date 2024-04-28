use crate::context::get_global_context;
use anyhow::Result;
use reqwest::Client;
use salvo::{handler, http::StatusCode, Request, Response};
use std::time::Duration;
use tracing::{error, info};

const TIMEOUT_SECS: u64 = 30u64;

#[handler]
pub async fn auth_handler(req: &mut Request, res: &mut Response) {
    if let Some(header_value) = req.headers().get("Authorization") {
        if let Ok(auth_value) = header_value.to_str() {
            let key = auth_value.trim_start_matches("Bearer ");
            let context = match get_global_context() {
                Ok(context) => context,
                Err(e) => {
                    error!("Error fetching repository: {e}");
                    res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
                    return;
                }
            };
            if let Ok(result) = is_valid(key, &context.env.auth_server).await {
                if result {
                    return;
                }
            }
        }
    }
    info!("Unauthorized");
    res.status_code(StatusCode::UNAUTHORIZED)
        .render("Unauthorized");
}

async fn is_valid(token: &str, server: &str) -> Result<bool> {
    let response = Client::builder()
        .build()?
        .get(format!("{server}/api/auth/is_authenticated/{token}"))
        .timeout(Duration::from_secs(TIMEOUT_SECS))
        .send()
        .await?;

    Ok(response.json::<bool>().await?)
}
