pub mod allergen;
pub mod recipe;
pub mod tag;
pub mod user;

pub const DATABASE_NAME: &str = "cooking_app";

pub trait CollectionName {
    #[must_use]
    fn get_collection_name() -> &'static str;
}
