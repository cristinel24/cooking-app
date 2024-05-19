pub mod put;
pub use put::put_recipe;
pub mod delete;
use crate::endpoints::EndpointResponse;
pub use delete::delete_recipe;

pub(crate) const SERVICE: &str = "recipe_saver";
