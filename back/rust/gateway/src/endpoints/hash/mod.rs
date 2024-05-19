pub mod get_primary;
pub use get_primary::get_hash_primary;
pub mod get_with;
pub use get_with::get_hash_with;

pub(crate) const SERVICE: &str = "hash";
