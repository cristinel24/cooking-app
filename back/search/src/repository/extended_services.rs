use crate::repository::service;
use anyhow::Result;
use async_trait::async_trait;
use bson::{doc, from_document, Bson};
use futures::TryStreamExt;
use crate::endpoints::{InputPayload, AggregationResponse};

#[async_trait]
pub trait RecipeDatabaseOperations {
    async fn find_by_tokens(&self, array: &[String]) -> Result<AggregationResponse>;
    async fn find_by_title(&self, title: String) -> Result<AggregationResponse>;
    async fn search(&self, payload: InputPayload) -> Result<AggregationResponse>;
}

#[async_trait]
impl RecipeDatabaseOperations for service::recipe::Service {
    async fn find_by_tokens(&self, array: &[String]) -> Result<AggregationResponse> {
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
                        "username": "$author.username",
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
            let response: AggregationResponse = from_document(document)?;
            return Ok(response);
        };

        Ok(AggregationResponse::default())
    }

    async fn find_by_title(&self, title: String) -> Result<AggregationResponse> {
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
                        "username": "$author.username",
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
            let response: AggregationResponse = from_document(document)?;
            return Ok(response);
        };

        Ok(AggregationResponse::default())
    }

    async fn search(&self, payload: InputPayload) -> Result<AggregationResponse> {
        let mut pipeline = vec![
            doc! {
                "$addFields": {
                    "ingredients": {
                        "$map": {
                            "input": "$ingredients",
                            "as": "ingredients",
                            "in": {
                                "$toLower": "$$ingredients",
                            }
                        }
                    },
                    "tags": {
                        "$map": {
                            "input": "$tags",
                            "as": "tags",
                            "in": {
                                "$toLower": "$$tags",
                            }
                        }
                    },
                    "allergens": {
                        "$map": {
                            "input": "$allergens",
                            "as": "allergens",
                            "in": {
                                "$toLower": "$$allergens",
                            }
                        }
                    },
                }
            }
        ];

        if let Some(filters) = payload.filters {
            let mut match_doc = doc! {};

            if let Some(ingredients) = filters.ingredients {
                match_doc.insert("ingredients", doc! { "$all": ingredients });
            }
            if let Some(tags) = filters.tags {
                match_doc.insert("tags", doc! { "$all": tags });
            }
            if let Some(blacklist) = filters.blacklist {
                if let Some(blacklisted_ingredients) = blacklist.ingredients {
                    match_doc.insert("ingredients", doc! { "$nin": blacklisted_ingredients });
                }
                if let Some(blacklisted_tags) = blacklist.tags {
                    match_doc.insert("tags", doc! { "$nin": blacklisted_tags });
                }
                if let Some(blacklisted_allergens) = blacklist.allergens {
                    match_doc.insert("allergens", doc! { "$nin": blacklisted_allergens });
                }
            }

            if let Some(prep_time) = filters.prep_time {
                match_doc.insert("prepTime", doc! { "$lte": prep_time });
            }
            if let Some(rating) = filters.rating {
                match_doc.insert("sumRating", doc! { "$gte": rating });
            }

            pipeline.push(doc! { "$match": match_doc });
        }

        pipeline.append(&mut vec![
            doc! { "$sort": { "updatedAt": -1 } },
            doc! {
                "$lookup": {
                    "from": "user",
                    "localField": "authorId",
                    "foreignField": "_id",
                    "as": "author"
                }
            },
            doc! {
                "$unwind": {
                    "path": "$author",
                    "preserveNullAndEmptyArrays": true
                }
            },
            doc! {
                "$match": {
                    "$or": [
                        {
                            "author.displayName": {
                                "$regex": &payload.data,
                                "$options": "i",
                            },
                        },
                        {
                            "author.username": {
                                "$regex": &payload.data,
                                "$options": "i",
                            },
                        },
                        {
                            "title": {
                                "$regex": &payload.data,
                                "$options": "i",
                            },
                        },
                        {
                            "description": {
                                "$regex": payload.data,
                                "$options": "i",
                            },
                        },
                    ]
                }
            },
            doc! {
                "$project": {
                    "_id": 0,
                    "author": {
                        "icon": "$author.icon",
                        "username": "$author.username",
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
                "$facet": {
                    "data": [
                        { "$skip": payload.page * payload.results_per_page },
                        { "$limit": payload.results_per_page },
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
            }
        ]);

        let mut cursor = self.collection.aggregate(pipeline, None).await?;
        if let Some(document) = cursor.try_next().await? {
            let response: AggregationResponse = from_document(document)?;
            return Ok(response);
        };

        Ok(AggregationResponse::default())
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