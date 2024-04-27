use crate::repository::cooking_app::CookingAppRepository;
use crate::CONTEXT;
use anyhow::Result;

pub mod cooking_app;
pub mod models;
pub mod service;

#[inline]
pub fn get_repository() -> Result<&'static CookingAppRepository> {
    CONTEXT.get().map_or_else(
        || Err(anyhow::Error::msg("Couldn't load CookingApp Context")),
        Ok,
    )
}
