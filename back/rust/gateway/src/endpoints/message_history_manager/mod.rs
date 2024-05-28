pub mod get;
pub use get::get_history;
pub mod post;
pub use post::post_history;
pub mod delete;
pub use delete::delete_history;

pub const SERVICE: &str = "message_history_manager";
