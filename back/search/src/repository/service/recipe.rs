use super::{super::models::recipe::Recipe, DATABASE_NAME};
use mongodb::{Client, Collection};

#[derive(Clone)]
pub struct Service {
    pub collection: Collection<Recipe>,
}

impl Service {
    #[must_use]
    pub fn new(client: &Client) -> Self {
        let collection = client
            .database(DATABASE_NAME)
            .collection::<Recipe>(Recipe::get_collection_name());

        Self { collection }
    }
}
