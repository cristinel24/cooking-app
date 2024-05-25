use salvo::{handler, http::StatusCode, Request, Response};
use tracing::info;

#[handler]
pub async fn auth_handler(req: &mut Request, res: &mut Response) {
    let headers = req.headers();

    if !(headers.contains_key("X-User-Id") && headers.contains_key("X-User-Roles")) {
        info!("Unauthorized");
        res.status_code(StatusCode::UNAUTHORIZED)
            .render("Unauthorized");
    }

    return;
}
