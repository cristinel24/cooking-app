use bson::doc;
use salvo::oapi::extract::JsonBody;
use salvo::prelude::{endpoint, Json, Writer};
use crate::endpoints::common::AiTokensPayload;
use crate::endpoints::{EndpointResponse, ErrorResponse, INTERNAL_SERVER_ERROR};
use crate::repository::get_context;

#[endpoint]
pub async fn search_ai_tokens(ai_tokens: JsonBody<AiTokensPayload>) -> Json<EndpointResponse> {
    let context = match get_context() {
        Ok(value) => value,
        Err(e) => {
            return Json(EndpointResponse::Error(ErrorResponse {
                message: e.to_string()
            }))
        }
    };



    return Json(EndpointResponse::default())
}