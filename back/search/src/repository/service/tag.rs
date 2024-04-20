use super::DATABASE_NAME;
use crate::repository::models::tag::Tag;
use mongodb::{Client, Collection};

#[derive(Clone)]
pub struct Service {
    pub(crate) collection: Collection<Tag>,
}

impl Service {
    #[must_use]
    pub fn new(client: &Client) -> Self {
        let collection = client
            .database(DATABASE_NAME)
            .collection::<Tag>(Tag::get_collection_name());

        Self { collection }
    }
}
