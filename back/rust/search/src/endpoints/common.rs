use crate::repository::{
    cooking_app::CookingAppRepository,
    models::recipe::Recipe,
    service::{allergen::Repository as AllergenRepository, tag::Repository as TagRepository},
};
use anyhow::Result;
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

pub const TOP: u32 = 10u32;

#[derive(Serialize, Deserialize, ToSchema, Debug)]
pub struct Filters {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub ingredients: Option<Vec<String>>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub blacklist: Option<BlacklistedFilters>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub tags: Option<Vec<String>>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub authors: Option<Vec<String>>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub prep_time: Option<u32>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub rating: Option<u32>,
}

#[derive(Serialize, Deserialize, ToSchema, Debug)]
pub struct BlacklistedFilters {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub ingredients: Option<Vec<String>>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub tags: Option<Vec<String>>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub allergens: Option<Vec<String>>,
}

#[derive(Debug)]
pub struct SearchRecipesParams {
    pub query: String,
    pub sort: String,
    pub order: i32,
    pub filters: Option<Filters>,
    pub start: u32,
    pub count: u32,
    pub tokens: Vec<String>,
}

pub async fn normalize_recipe(
    recipe: &mut Recipe,
    repository: &CookingAppRepository,
) -> Result<()> {
    let top_tags = repository
        .tag_collection
        .filter_top_x_tags(recipe.tags.clone(), TOP)
        .await?;

    if let Some(top) = top_tags {
        recipe.tags = top;
    }
    let top_tags = repository
        .allergen_collection
        .filter_top_x_allergens(recipe.allergens.clone(), TOP)
        .await?;

    if let Some(top) = top_tags {
        recipe.allergens = top;
    }
    Ok(())
}
