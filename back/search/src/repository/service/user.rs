use super::{super::models::user::User, DATABASE_NAME};
use mongodb::{Client, Collection};

#[derive(Clone)]
pub struct Service {
    pub collection: Collection<User>,
}

impl Service {
    #[must_use]
    pub fn new(client: &Client) -> Self {
        let collection = client
            .database(DATABASE_NAME)
            .collection::<User>(User::get_collection_name());

        Self { collection }
    }
}
