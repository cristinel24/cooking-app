use super::{super::models::user::User, CollectionName, DATABASE_NAME};
use crate::endpoints::{user::SearchUsersParams, AggregationResponse};
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
    async fn search(&self, params: SearchUsersParams) -> Result<AggregationResponse<T>>;
}

impl Repository<User> for Service {
    async fn search(&self, params: SearchUsersParams) -> Result<AggregationResponse<User>> {
        let pipeline = vec![
            doc! {
                "$match": {
                    "$or": [
                        { "username": { "$regex": &params.query, "$options": "i" } },
                        { "displayName": { "$regex": params.query, "$options": "i" } }
                    ]
                }
            },
            doc! {
                "$project": {
                    "_id": 0,
                    "id": 1,
                    "icon": 1,
                    "displayName": 1,
                    "username": 1,
                    "roles": 1,
                    "ratingAvg": {
                        "$cond": {
                            "if": { "$eq": ["$ratingCount", 0] },
                            "then": 0,
                            "else": { "$divide": ["$ratingSum", "$ratingCount"] }
                        }
                    }
                }
            },
            doc! { "$sort": { params.sort: params.order } },
            doc! {
                "$facet": {
                    "data": [
                        { "$skip": params.start * params.count },
                        { "$limit": params.count },
                    ],
                    "total": [
                        { "$count": "count" }
                    ]
                }
            },
            doc! { "$unwind": { "path": "$total" } },
            doc! {
                "$project": {
                    "data": 1,
                    "count": "$total.count",
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
