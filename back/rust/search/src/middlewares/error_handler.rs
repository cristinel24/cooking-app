use crate::endpoints::{ErrorResponse, INTERNAL_SERVER_ERROR};
use salvo::{
    http::{ResBody, StatusCode},
    prelude::Json,
    handler, Depot, FlowCtrl, Request, Response
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
        if let ResBody::Error(error) = &res.body {
            let error = ErrorResponse {
                message: error.brief.clone(),
            };
            error!("{error:?}");
            res.status_code(StatusCode::BAD_REQUEST);
            res.render(Json(error));
        }
    } else {
        let error = ErrorResponse {
            message: INTERNAL_SERVER_ERROR.to_string(),
        };
        error!("{error:?}");
    }
}
