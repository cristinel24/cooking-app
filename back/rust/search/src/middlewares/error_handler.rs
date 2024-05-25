use crate::endpoints::{ErrorCodes, ErrorResponse};
use salvo::{
    handler,
    http::{ResBody, StatusCode},
    prelude::Json,
    Depot, FlowCtrl, Request, Response,
};
use tracing::{error, info};

#[handler]
pub async fn error_handler(
    req: &mut Request,
    res: &mut Response,
    depot: &mut Depot,
    ctrl: &mut FlowCtrl,
) {
    info!("{} {}", req.method(), req.uri());

    if ctrl.call_next(req, depot, res).await {
        if let ResBody::Error(_) = &res.body {
            let error = ErrorResponse {
                error_code: ErrorCodes::BadData as u32,
            };
            error!("{error:?}");
            res.status_code(StatusCode::BAD_REQUEST);
            res.render(Json(error));
        }
    } else {
        let error = ErrorResponse {
            error_code: ErrorCodes::Unknown as u32,
        };
        error!("{error:?}");
    }
}
