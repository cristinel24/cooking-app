pub mod put;
pub use put::put_recipe;
pub mod delete;
pub use delete::delete_recipe;
use crate::endpoints::EndpointResponse;

pub(crate) const SERVICE: &str = "recipe_saver";
