pub mod delete;
pub use delete::delete_item_search_history;
pub mod get;
pub use get::get_search_history_endpoint;
pub mod post;
pub use post::post_in_search_history;

pub const SERVICE: &str = "search_history_manager";
