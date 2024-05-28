pub mod get_follow_count;
pub use get_follow_count::get_followers_count;
pub mod get_followers;
pub use get_followers::get_all_followers;
pub mod get_following_count;
pub use get_following_count::get_user_following_count;
pub mod get_following;
pub use get_following::get_all_following;
pub mod post_new_follower;
pub use post_new_follower::post_new_following_user;
pub mod delete_following;
pub use delete_following::delete_following_user;

pub const SERVICE: &str = "follow_manager";
