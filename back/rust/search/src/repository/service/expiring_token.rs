use crate::repository::{
    models::expiring_token::ExpiringToken,
    service::{CollectionName, DATABASE_NAME},
};
use anyhow::Result;
use async_trait::async_trait;
use bson::doc;
use mongodb::{Client, Collection};

#[derive(Clone)]
pub struct Service {
    pub collection: Collection<ExpiringToken>,
}

impl Service {
    #[must_use]
    pub fn new(client: &Client) -> Self {
        let collection = client
            .database(DATABASE_NAME)
            .collection::<ExpiringToken>(ExpiringToken::get_collection_name());

        Self { collection }
    }
}

#[async_trait]
pub trait Repository {
    async fn is_valid(&self, token: &str, r#type: &str) -> Result<bool>;
}

#[async_trait]
impl Repository for Service {
    async fn is_valid(&self, token: &str, r#type: &str) -> Result<bool> {
        let query = doc! {
            "value": token,
            "type": r#type,
        };

        let result = self.collection.find_one(query, None).await?;
        Ok(result.is_some())
    }
}
