use crate::repository::models::recipe::Recipe;
use crate::repository::service;
use anyhow::{Context, Result};
use async_trait::async_trait;
use bson::{doc, from_document};
use futures::TryStreamExt;

#[async_trait]
pub trait RecipeDatabaseOperations {
    async fn find_by_tokens(&self, array: &[String]) -> Result<Vec<Recipe>>;
}

#[async_trait]
impl RecipeDatabaseOperations for service::recipe::Service {
    async fn find_by_tokens(&self, array: &[String]) -> Result<Vec<Recipe>> {
        let pipeline = vec![
            doc! { "$match": { "tokens": { "$in": array} } },
            doc! { "$lookup": {
                "from": "user",
                "localField": "authorId",
                "foreignField": "_id",
                "as": "author"
            }},
            doc! { "$unwind": {
                "path": "$author"
            } },
            doc! {
                "$project": {
                    "_id": 1,
                    "author": {
                        "icon": "$author.icon",
                        "username": "$author.login.username",
                        "displayName": "$author.displayName",
                        "roles": "$author.roles"
                    },
                    "title": 1,
                    "description": { "$substrCP": ["$description", 0, 100] },
                    "prepTime": 1,
                    "allergens": { "$slice": [ "$allergens", 10 ] } ,
                    "tags": { "$slice": [ "$tags", 10 ] }
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
        let mut recipes: Vec<Recipe> = Vec::new();
        while let Some(document) = cursor.try_next().await? {
            let recipe: Recipe = from_document(document)?;
            recipes.push(recipe);
        }

        Ok(recipes)
    }
}
