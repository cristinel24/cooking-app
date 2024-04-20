use async_trait::async_trait;
use anyhow::Result;
use bson::doc;
use crate::repository::service;


#[async_trait]
pub trait DatabaseOperations {
    async fn find_tokens(&self, array: &[String]) -> Result<Vec<String>>;
}

#[async_trait]
impl DatabaseOperations for service::recipe::Service {
    async fn find_tokens(&self, array: &[String]) -> Result<Vec<String>> {
        let query = doc! { "tokens" : { "$in": array } };

        let docs = self
            .collection
            .find(query, None)
            .await?;

        Ok(Vec::new())
    }

}