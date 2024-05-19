use crate::repository::{
    cooking_app::CookingAppRepository,
    models::recipe::Recipe,
    service::{allergen::Repository as AllergenRepository, tag::Repository as TagRepository},
};
use anyhow::Result;

pub const TOP: u32 = 10u32;

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
