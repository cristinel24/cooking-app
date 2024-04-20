use crate::repository::cooking_app::CookingAppRepository;
use crate::CONTEXT;
use anyhow::Result;

pub mod cooking_app;
pub mod extended_services;
pub mod models;
pub mod service;

#[inline]
pub fn get_context() -> Result<&'static CookingAppRepository> {
    CONTEXT.get().map_or_else(
        || Err(anyhow::Error::msg("Couldn't load CookingApp Context")),
        Ok,
    )
}
