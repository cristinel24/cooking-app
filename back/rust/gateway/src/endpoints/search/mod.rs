pub mod ai;
pub use ai::ai_endpoint;
pub mod recipes;
pub use recipes::recipes_endpoint;
pub mod users;
pub use users::users_endpoint;

pub const SERVICE: &str = "search";