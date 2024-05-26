pub mod delete;

pub use delete::delete_rating_endpoint;
pub mod get;
pub use get::get_rating_endpoint;
pub mod patch;
pub use patch::patch_rating_endpoint;
pub mod put;
pub use put::post_rating_endpoint;

pub(crate) const SERVICE: &str = "rating_manager";
