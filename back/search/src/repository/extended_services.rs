use crate::endpoints::recipe::RecipeResponsePayload;
use crate::repository::service;
use anyhow::Result;
use async_trait::async_trait;
use bson::{doc, from_document, Bson};
use futures::TryStreamExt;

#[async_trait]
pub trait RecipeDatabaseOperations {
    async fn find_by_tokens(&self, array: &[String]) -> Result<RecipeResponsePayload>;
    async fn find_by_title(&self, title: String) -> Result<RecipeResponsePayload>;
}

#[async_trait]
impl RecipeDatabaseOperations for service::recipe::Service {
    async fn find_by_tokens(&self, array: &[String]) -> Result<RecipeResponsePayload> {
        let lower_cased_tokens: Vec<String> =
            array.iter().map(|item| item.to_lowercase()).collect();
        let pipeline = vec![
            doc! {
                "$addFields": {
                    "lowercase_tokens": {
                        "$map": {
                            "input": "$tokens",
                            "as": "token",
                            "in": { "$toLower": "$$token" }
                        }
                    }
                }
            },
            doc! { "$match": { "lowercase_tokens": { "$in": lower_cased_tokens} } },
            doc! {
                "$lookup": {
                    "from": "user",
                    "localField": "authorId",
                    "foreignField": "_id",
                    "as": "author"
                }
            },
            doc! { "$unwind": { "path": "$author" } },
            doc! {
                "$project": {
                    "_id": 0,
                    "author": {
                        "icon": "$author.icon",
                        "username": "$author.login.username",
                        "displayName": "$author.displayName",
                        "roles": "$author.roles"
                    },
                    "title": 1,
                    "description": { "$substrCP": ["$description", 0, 100] },
                    "prepTime": 1,
                    "allergens": 1,
                    "tags": 1
                }
            },
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
            let response: RecipeResponsePayload = from_document(document)?;
            return Ok(response);
        };

        Ok(RecipeResponsePayload::default())
    }

    async fn find_by_title(&self, title: String) -> Result<RecipeResponsePayload> {
        let pipeline = vec![
            doc! {
                "$match": {
                    "$text": {
                        "$search": title
                    }
                }
            },
            doc! {
                "$lookup": {
                    "from": "user",
                    "localField": "authorId",
                    "foreignField": "_id",
                    "as": "author"
                }
            },
            doc! { "$unwind": { "path": "$author" } },
            doc! {
                "$project": {
                    "_id": 0,
                    "author": {
                        "icon": "$author.icon",
                        "username": "$author.login.username",
                        "displayName": "$author.displayName",
                        "roles": "$author.roles"
                    },
                    "title": 1,
                    "description": { "$substrCP": ["$description", 0, 100] },
                    "prepTime": 1,
                    "allergens": 1,
                    "tags": 1
                }
            },
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
            let response: RecipeResponsePayload = from_document(document)?;
            return Ok(response);
        };

        Ok(RecipeResponsePayload::default())
    }
}

#[async_trait]
pub trait TagDatabaseOperations {
    async fn filter_top_x_tags(
        &self,
        tags: Vec<String>,
        number: u32,
    ) -> Result<Option<Vec<String>>>;
}

#[async_trait]
impl TagDatabaseOperations for service::tag::Service {
    async fn filter_top_x_tags(
        &self,
        tags: Vec<String>,
        number: u32,
    ) -> Result<Option<Vec<String>>> {
        let pipeline = vec![
            doc! { "$match": { "tag": { "$in": tags } } },
            doc! { "$sort": { "counter" : -1 } },
            doc! { "$limit": number },
            doc! { "$project": { "tag": 1, "_id": 0 } },
            doc! { "$group": { "_id": null, "tags": { "$push": "$tag" } } },
        ];

        let mut cursor = self.collection.aggregate(pipeline, None).await?;
        let mut results: Vec<String> = Vec::new();
        if let Some(result) = cursor.try_next().await? {
            if let Some(Bson::Array(tags)) = result.get("tags") {
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

#[async_trait]
pub trait AllergenDatabaseOperations {
    async fn filter_top_x_allergens(
        &self,
        allergens: Vec<String>,
        number: u32,
    ) -> Result<Option<Vec<String>>>;
}

#[async_trait]
impl AllergenDatabaseOperations for service::allergen::Service {
    async fn filter_top_x_allergens(
        &self,
        allergens: Vec<String>,
        number: u32,
    ) -> Result<Option<Vec<String>>> {
        let pipeline = vec![
            doc! { "$match": { "allergen": { "$in": allergens } } },
            doc! { "$sort": { "counter" : -1 } },
            doc! { "$limit": number },
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
