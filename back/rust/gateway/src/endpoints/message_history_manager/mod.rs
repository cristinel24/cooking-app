pub mod get;
pub use get::get_history;
pub mod put;
pub use put::put_history;
pub mod delete;
pub use delete::delete_history;

pub const SERVICE: &str = "message_history";
