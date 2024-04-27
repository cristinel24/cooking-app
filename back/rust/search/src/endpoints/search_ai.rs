use crate::{
    get_context,
    context::get_global_context,
    endpoints::{
        common::normalize_recipe, EndpointResponse, ErrorResponse, InputPayload, SearchResponse,
        INTERNAL_SERVER_ERROR,
    },
    repository::{
        models::recipe::Recipe,
        service::{recipe::Repository as RecipeRepository, user::Repository as UserRepository},
    },
};
use salvo::{
    oapi::{endpoint, extract::JsonBody},
    prelude::{Json, Response, StatusCode, Writer},
};
use std::time::Duration;
use serde::Deserialize;
use reqwest::{Client, Url};
use anyhow::Result;
use tracing::error;

const TIMEOUT_SECS: u64 = 30u64;

#[endpoint]
pub async fn search_ai(
    payload: JsonBody<InputPayload>,
    res: &mut Response,
) -> Json<EndpointResponse<Recipe>> {
    let context = get_context!(res);

    let tokens = match get_ai_tokens(&payload.data, &context.env.ai_server).await {
        Ok(value) => value,
        Err(e) => {
            error!("Error: {e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            return Json(EndpointResponse::Error(ErrorResponse {
                message: INTERNAL_SERVER_ERROR.to_string(),
            }));
        }
    };


    let recipes = match context.repository.recipe_collection.find_by_tokens(&tokens).await {
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
            value
        }
        Err(e) => {
            error!("Error: {e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            return Json(EndpointResponse::Error(ErrorResponse {
                message: e.to_string(),
            }));
        }
    };

    let users = match context.repository.user_collection.find_by_name(&payload.data).await {
        Ok(value) => value,
        Err(e) => {
            error!("Error: {e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            return Json(EndpointResponse::Error(ErrorResponse {
                message: e.to_string(),
            }));
        }
    };

    Json(EndpointResponse::SuccessSearch(SearchResponse {
        recipes,
        users,
    }))
}

#[derive(Deserialize, Debug)]
struct AiResponse {
    pub tags: Vec<String>,
}

pub async fn get_ai_tokens(query: &String, server: &str) -> Result<Vec<String>> {
    let encoded_url = Url::parse(format!("{server}/api/tokenize/user_query/{query}").as_str())?;
    let response = Client::builder()
        .build()?
        .get(encoded_url)
        .timeout(Duration::from_secs(TIMEOUT_SECS))
        .send()
        .await?;

    let result = response.json::<AiResponse>().await?;
    Ok(result.tags)
}
