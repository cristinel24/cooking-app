pub mod delete_rating;
pub use delete_rating::delete_rating_endpoint;
pub mod delete_recipe_ratings;
pub use delete_recipe_ratings::delete_recipe_ratings_endpoint;
pub mod get_rating_comments;
pub use get_rating_comments::get_rating_comments_endpoint;
pub mod get_recipe_comments;
pub use get_recipe_comments::get_recipe_comments_endpoint;
pub mod get_rating_by_id;
pub use get_rating_by_id::get_rating_by_id_endpoint;
pub mod get_rating_by_recipe_and_author;
pub use get_rating_by_recipe_and_author::get_rating_by_recipe_and_author_endpoint;
pub mod patch;
pub use patch::patch_rating_endpoint;
pub mod post;
pub use post::post_rating_endpoint;

pub(crate) const SERVICE: &str = "rating_manager";
