pub mod replace_ingredient;
pub use replace_ingredient::replace_ingredient_route;
pub mod chatbot;
pub use chatbot::chatbot_route;

pub const SERVICE: &str = "ai";
