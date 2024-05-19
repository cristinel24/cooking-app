pub mod verify;
pub use verify::verify_account;
pub mod request;
pub use request::request_change;

pub const SERVICE: &str = "email";