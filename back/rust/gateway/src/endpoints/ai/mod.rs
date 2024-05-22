pub mod tokenize;
pub use tokenize::replace_ingredient;
pub mod chatbot;
pub use chatbot::ai_talk;

pub const SERVICE: &str = "ai";
