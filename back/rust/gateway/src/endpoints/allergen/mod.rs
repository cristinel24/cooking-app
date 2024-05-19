pub mod get;
pub use get::get_allergen_item;
pub mod post;
pub use post::post_allergen_item;
pub mod delete;
pub use delete::delete_allergen_item;

pub(crate) const SERVICE: &str = "allergen";
