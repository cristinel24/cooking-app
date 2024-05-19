pub mod get_user;
pub use get_user::get_user_data_item;
pub mod get_user_card;
pub use get_user_card::get_user_card_item;
pub mod get_user_profile;
pub use get_user_profile::get_user_profile_item;
pub mod post_user_card;
pub use post_user_card::post_user_card_item;

pub const SERVICE: &str = "user_retriever";
