pub mod get;
pub use get::get_tag_item;
pub mod post;
pub use post::post_tag_item;
pub mod delete;
pub use delete::delete_tag_item;

pub(crate) const SERVICE: &str = "tag";
