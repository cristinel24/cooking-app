use super::DATABASE_NAME;
use crate::repository::models::allergen::Allergen;
use mongodb::{Client, Collection};

#[derive(Clone)]
pub struct Service {
    pub(crate) collection: Collection<Allergen>,
}

impl Service {
    #[must_use]
    pub fn new(client: &Client) -> Self {
        let collection = client
            .database(DATABASE_NAME)
            .collection::<Allergen>(Allergen::get_collection_name());

        Self { collection }
    }
}
