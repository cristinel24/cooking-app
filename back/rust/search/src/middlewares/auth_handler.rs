use salvo::{handler, http::StatusCode, writing::Json, Request, Response};
use tracing::info;

use crate::endpoints::{ErrorCodes, ErrorResponse};

#[handler]
pub async fn auth_handler(req: &mut Request, res: &mut Response) {
    let headers = req.headers();

    if !(headers.contains_key("X-User-Id") && headers.contains_key("X-User-Roles")) {
        info!("Unauthorized");
        res.status_code(StatusCode::UNAUTHORIZED)
            .render(Json(ErrorResponse {
                error_code: ErrorCodes::Unauthorized as u32,
            }));
    }

    return;
}
