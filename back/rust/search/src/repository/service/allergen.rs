use super::DATABASE_NAME;
use crate::repository::models::allergen::Allergen;
use anyhow::Result;
use async_trait::async_trait;
use bson::{doc, Bson};
use futures::TryStreamExt;
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

#[async_trait]
pub trait Repository {
    async fn filter_top_x_allergens(
        &self,
        allergens: Vec<String>,
        number: u32,
    ) -> Result<Option<Vec<String>>>;
}

#[async_trait]
impl Repository for Service {
    async fn filter_top_x_allergens(
        &self,
        allergens: Vec<String>,
        number: u32,
    ) -> anyhow::Result<Option<Vec<String>>> {
        let pipeline = vec![
            doc! { "$addFields": { "allergen": { "$toLower": "$allergen"} } },
            doc! { "$match": { "allergen": { "$in": allergens } } },
            doc! { "$sort": { "counter" : -1 } },
            doc! { "$limit": number as i32},
            doc! { "$project": { "allergen": 1, "_id": 0 } },
            doc! { "$group": { "_id": null, "allergens": { "$push": "$allergen" } } },
        ];

        let mut cursor = self.collection.aggregate(pipeline, None).await?;
        let mut results: Vec<String> = Vec::new();
        if let Some(result) = cursor.try_next().await? {
            if let Some(Bson::Array(tags)) = result.get("allergens") {
                results = tags
                    .iter()
                    .filter_map(|item| {
                        if let Bson::String(name) = item {
                            Some(name.clone())
                        } else {
                            None
                        }
                    })
                    .collect();
            }
            Ok::<Option<Vec<String>>, anyhow::Error>(Some(results))
        } else {
            Ok(None)
        }
    }
}
