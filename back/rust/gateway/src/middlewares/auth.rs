use salvo::{handler, Depot, FlowCtrl, Request, Response};

pub const AUTH_HEADER: &str = "Authorization";
pub const HEADER_KEYS: [&str; 2] = ["X-User-Id", "X-User-Roles"];

#[handler]
pub async fn auth_middleware(
    req: &mut Request,
    depot: &mut Depot,
    res: &mut Response,
    ctrl: &mut FlowCtrl,
) {
    let headers = req.headers_mut();
    let _authorization = headers.get::<String>(AUTH_HEADER.to_string());
    headers.remove("Content-length");
    // let headers = HEADER_KEYS.iter()
    //     .map(|header| (header, None)) // TODO: call some serice to get user_id/roles
    //     .collect::<Vec<_>>();
    ctrl.call_next(req, depot, res).await;
}
