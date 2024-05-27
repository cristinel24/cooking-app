use crate::endpoints::{get_response, EndpointResponse};
use crate::models::token_validator::Success;
use crate::models::ErrorResponse;
use reqwest::{Method, StatusCode};
use salvo::http::HeaderValue;
use salvo::prelude::Json;
use salvo::{handler, Depot, FlowCtrl, Request, Response};


pub const AUTH_HEADER: &str = "Authorization";
const AUTH_SERVICE: &str = "token_validator";

#[handler]
pub async fn auth_middleware(
    req: &mut Request,
    depot: &mut Depot,
    res: &mut Response,
    ctrl: &mut FlowCtrl,
) {
    let headers = req.headers_mut();
    headers.remove("Content-length");
    let authorization = headers.get::<String>(AUTH_HEADER.to_string());

    if let Some(authorization) = authorization {
        let authorization = authorization.to_str().unwrap_or_default();
        let Ok(response) = get_response::<&str, &str, Success>(
            Method::GET,
            format!("{AUTH_SERVICE}/session/{authorization}"),
            None,
            None,
            None,
            false,
        )
        .await
        else {
            res.status_code(StatusCode::UNAUTHORIZED);
            res.render(Json(ErrorResponse {
                error_code: u32::from(StatusCode::UNAUTHORIZED.as_u16()),
            }));
            return;
        };
        let EndpointResponse::Ok(response) = response else {
            res.status_code(StatusCode::UNAUTHORIZED);
            res.render(Json(ErrorResponse {
                error_code: u32::from(StatusCode::UNAUTHORIZED.as_u16()),
            }));
            return;
        };
        let x_user_id = HeaderValue::from_str(&response.user_id);
        if let Ok(x_user_id) = x_user_id {
            headers.append("X-User-Id", x_user_id);
        }
        headers.append("X-User-Roles", HeaderValue::from(response.user_roles));
    };

    ctrl.call_next(req, depot, res).await;
}
