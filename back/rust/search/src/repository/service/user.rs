use super::{super::models::user::User, CollectionName, DATABASE_NAME};
use crate::endpoints::AggregationResponse;
use anyhow::Result;
use bson::{doc, from_document};
use futures::TryStreamExt;
use mongodb::{Client, Collection};
use serde::Serialize;

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

pub trait Repository<T: Serialize> {
    async fn find_by_name(&self, data: &str) -> Result<AggregationResponse<T>>;
}

impl Repository<User> for Service {
    async fn find_by_name(&self, data: &str) -> Result<AggregationResponse<User>> {
        let pipeline = vec![
            doc! {
                "$match": {
                    "$or": [
                        { "username": { "$regex": data, "$options": "i" } },
                        { "displayName": { "$regex": data, "$options": "i" } }
                    ]
                }
            },
            doc! {
                "$project": {
                    "_id": 0,
                    "icon": 1,
                    "displayName": 1,
                    "username": 1,
                    "roles": 1,
                    "rating": {
                        "$cond": {
                            "if": { "$eq": ["$ratingCount", 0] },
                            "then": 0,
                            "else": { "$divide": ["$ratingSum", "$ratingCount"] }
                        }
                    }
                }
            },
            doc! { "$sort": { "rating": -1 } },
            doc! {
                "$group": {
                    "_id": null,
                    "data": { "$push": "$$ROOT" },
                    "count": { "$sum": 1 }
                }
            },
            doc! {
                "$project": {
                    "_id": 0,
                    "data": 1,
                    "count": 1
                }
            },
        ];
        let mut cursor = self.collection.aggregate(pipeline, None).await?;
        if let Some(document) = cursor.try_next().await? {
            let users_aggregation: AggregationResponse<User> = from_document(document)?;
            return Ok(users_aggregation);
        }
        Ok(AggregationResponse::default())
    }
}
