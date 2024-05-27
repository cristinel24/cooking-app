pub mod tokenize;
pub use tokenize::replace_ingredient;
pub mod chatbot;
pub use chatbot::talk;

pub const SERVICE: &str = "ai";
