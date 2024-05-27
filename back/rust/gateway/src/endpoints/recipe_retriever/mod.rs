pub mod get_recipe;
pub use get_recipe::get_full_recipe;
pub mod get_recipe_card;
pub use get_recipe_card::get_card_recipe;

pub const SERVICE: &str = "recipe_retriever";
