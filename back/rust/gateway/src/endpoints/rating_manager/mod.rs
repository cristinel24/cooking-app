pub mod delete;
pub use delete::delete_rating_endpoint;
pub mod delete_all;
pub use delete_all::delete_recipe_ratings_endpoint;
pub mod get_all;
pub use get_all::get_ratings_endpoint;
pub mod get;
pub use get::get_rating_endpoint;
pub mod get_by_author;
pub use get_by_author::get_rating_by_author_endpoint;
pub mod patch;
pub use patch::patch_rating_endpoint;
pub mod post;
pub use post::post_rating_endpoint;

pub(crate) const SERVICE: &str = "rating_manager";