use crate::{
    context::get_repository,
    repository::service::expiring_token::Repository
};
use salvo::{handler, http::StatusCode, Request, Response};
use tracing::error;

#[handler]
pub async fn auth_handler(req: &mut Request, res: &mut Response) {
    if let Some(header_value) = req.headers().get("Authorization") {
        if let Ok(auth_value) = header_value.to_str() {
            let key = auth_value.trim_start_matches("Bearer ");
            let context = match get_repository() {
                Ok(context) => context,
                Err(e) => {
                    error!("Error fetching repository: {e}");
                    res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
                    return;
                }
            };
            match context
                .repository
                .expiring_token_collection
                .is_valid(key, "session")
                .await
            {
                Ok(value) => {
                    if value {
                        return;
                    }
                    error!("Error: Authorization Token Invalid!");
                }
                Err(e) => error!("Error: {e}"),
            }
        }
    }
    res.status_code(StatusCode::UNAUTHORIZED)
        .render("Unauthorized");
}
