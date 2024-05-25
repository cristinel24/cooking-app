use crate::{
    context::get_global_context,
    endpoints::{
        ai::SearchAiPayload, common::normalize_recipe, EndpointResponse, ErrorResponse,
        INTERNAL_SERVER_ERROR,
    },
    get_endpoint_context,
    repository::{models::recipe::Recipe, service::recipe::Repository as RecipeRepository},
};
use anyhow::Result;
use reqwest::{Client, Url};
use salvo::{
    oapi::{endpoint, extract::JsonBody},
    prelude::{Json, Response, StatusCode, Writer},
};
use serde::Deserialize;
use std::time::Duration;
use tracing::error;

const TIMEOUT_SECS: u64 = 30u64;

#[endpoint]
pub async fn search_ai(
    payload: JsonBody<SearchAiPayload>,
    res: &mut Response,
) -> Json<EndpointResponse<Recipe>> {
    let context = get_endpoint_context!(res);

    let tokens = match get_ai_tokens(&payload.query, &context.env.ai_api_url).await {
        Ok(value) => value,
        Err(e) => {
            error!("Error: {e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            return Json(EndpointResponse::Error(ErrorResponse {
                message: INTERNAL_SERVER_ERROR.to_string(),
            }));
        }
    };

    match context
        .repository
        .recipe_collection
        .search(payload.into_inner().to_params(tokens))
        .await
    {
        Ok(mut value) => {
            for recipe in &mut value.data {
                if let Err(e) = normalize_recipe(recipe, &context.repository).await {
                    error!("Error: {e}");
                    res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
                    return Json(EndpointResponse::Error(ErrorResponse {
                        message: INTERNAL_SERVER_ERROR.to_string(),
                    }));
                }
            }
            Json(EndpointResponse::Success(value))
        }
        Err(e) => {
            error!("Error: {e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            Json(EndpointResponse::Error(ErrorResponse {
                message: e.to_string(),
            }))
        }
    }
}

#[derive(Deserialize, Debug)]
struct AiResponse {
    pub tokens: Vec<String>,
}

pub async fn get_ai_tokens(query: &String, server: &str) -> Result<Vec<String>> {
    let encoded_url = Url::parse(format!("{server}/tokenize/user_query").as_str())?;
    let response = Client::builder()
        .build()?
        .get(encoded_url)
        .query(&[("query", query)])
        .timeout(Duration::from_secs(TIMEOUT_SECS))
        .send()
        .await?;

    let result = response.json::<AiResponse>().await?;
    Ok(result.tokens)
}
