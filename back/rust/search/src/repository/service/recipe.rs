use super::{super::models::recipe::Recipe, CollectionName, DATABASE_NAME};
use crate::endpoints::{common::SearchRecipesParams, AggregationResponse};
use anyhow::Result;
use async_trait::async_trait;
use bson::{doc, from_document, Document};
use futures::TryStreamExt;
use mongodb::{Client, Collection};
use serde::Serialize;

#[derive(Clone)]
pub struct Service {
    pub(crate) collection: Collection<Recipe>,
}

impl Service {
    #[must_use]
    pub fn new(client: &Client) -> Self {
        let collection = client
            .database(DATABASE_NAME)
            .collection::<Recipe>(Recipe::get_collection_name());

        Self { collection }
    }
}

#[async_trait]
pub trait Repository<T: Serialize> {
    async fn find_by_tokens(&self, array: &[String]) -> Result<AggregationResponse<T>>;
    async fn find_by_title(&self, title: String) -> Result<AggregationResponse<T>>;
    async fn search(&self, payload: SearchRecipesParams) -> Result<AggregationResponse<T>>;
}

#[async_trait]
impl Repository<Recipe> for Service {
    async fn find_by_tokens(&self, array: &[String]) -> Result<AggregationResponse<Recipe>> {
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
                    "foreignField": "id",
                    "as": "author"
                }
            },
            doc! { "$unwind": { "path": "$author" } },
            doc! {
                "$project": {
                    "_id": 0,
                    "id": 1,
                    "author": {
                        "id": "$author.id",
                        "icon": "$author.icon",
                        "displayName": "$author.displayName",
                        "username": "$author.username",
                        "roles": "$author.roles",
                        "ratingAvg": {
                            "$cond": {
                                "if": { "$eq": ["$ratingCount", 0] },
                                "then": 0,
                                "else": { "$divide": ["$ratingSum", "$ratingCount"] }
                            }
                        }
                    },
                    "title": 1,
                    "ratingAvg": {
                        "$cond": {
                            "if": { "$eq": ["$ratingCount", 0] },
                            "then": 0,
                            "else": { "$divide": ["$ratingSum", "$ratingCount"] }
                        }
                    },
                    "description": { "$substrCP": ["$description", 0, 100] },
                    "prepTime": 1,
                    "allergens": 1,
                    "tags": 1,
                    "thumbnail": 1,
                    "viewCount": 1
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
            let response: AggregationResponse<Recipe> = from_document(document)?;
            return Ok(response);
        };

        Ok(AggregationResponse::default())
    }

    async fn find_by_title(&self, title: String) -> Result<AggregationResponse<Recipe>> {
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
                    "foreignField": "id",
                    "as": "author"
                }
            },
            doc! { "$unwind": { "path": "$author" } },
            doc! {
                "$project": {
                    "_id": 0,
                    "id": 1,
                    "author": {
                        "id": "$author.id",
                        "icon": "$author.icon",
                        "displayName": "$author.displayName",
                        "username": "$author.username",
                        "roles": "$author.roles",
                        "ratingAvg": {
                            "$cond": {
                                "if": { "$eq": ["$ratingCount", 0] },
                                "then": 0,
                                "else": { "$divide": ["$ratingSum", "$ratingCount"] }
                            }
                        }
                    },
                    "title": 1,
                    "ratingAvg": {
                        "$cond": {
                            "if": { "$eq": ["$ratingCount", 0] },
                            "then": 0,
                            "else": { "$divide": ["$ratingSum", "$ratingCount"] }
                        }
                    },
                    "description": { "$substrCP": ["$description", 0, 100] },
                    "prepTime": 1,
                    "allergens": 1,
                    "tags": 1,
                    "thumbnail": 1,
                    "viewCount": 1
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
            let response: AggregationResponse<Recipe> = from_document(document)?;
            return Ok(response);
        };

        Ok(AggregationResponse::default())
    }

    async fn search(&self, params: SearchRecipesParams) -> Result<AggregationResponse<Recipe>> {
        let mut pipeline = vec![];

        let mut fields = doc! {
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
        };

        if !params.tokens.is_empty() {
            println!("{:?}", params.tokens);
            fields.insert(
                "lowercase_tokens",
                doc! {
                    "$map": {
                        "input": "$tokens",
                        "as": "token",
                        "in": { "$toLower": "$$token" }
                    }
                },
            );
        }

        pipeline.push(doc! { "$addFields": fields });

        let mut matched_authors: Option<Document> = None;
        let mut match_doc = doc! {};

        if !params.tokens.is_empty() {
            match_doc.insert("lowercase_tokens", doc! { "$in": params.tokens });
        }

        if let Some(filters) = params.filters {
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
                match_doc.insert("ratingSum", doc! { "$gte": rating });
            }

            pipeline.push(doc! { "$match": match_doc });

            if let Some(users) = filters.authors {
                let or_conditions = users
                    .into_iter()
                    .flat_map(|user| {
                        vec![
                            doc! {"author.displayName": { "$regex": &user, "$options": "i"} },
                            doc! {"author.username": { "$regex": user, "$options": "i", } },
                        ]
                    })
                    .collect::<Vec<_>>();
                matched_authors = Some(doc! {
                    "$match": {
                        "$or": or_conditions
                    }
                })
            }
        }

        pipeline.append(&mut vec![
            doc! { "$sort": { params.sort: params.order } },
            doc! {
                "$lookup": {
                    "from": "user",
                    "localField": "authorId",
                    "foreignField": "id",
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
                                "$regex": &params.query,
                                "$options": "i",
                            },
                        },
                        {
                            "author.username": {
                                "$regex": &params.query,
                                "$options": "i",
                            },
                        },
                        {
                            "title": {
                                "$regex": &params.query,
                                "$options": "i",
                            },
                        },
                        {
                            "description": {
                                "$regex": params.query,
                                "$options": "i",
                            },
                        },
                    ]
                }
            },
        ]);

        if let Some(user_pipe) = matched_authors {
            pipeline.push(user_pipe);
        };

        pipeline.append(&mut vec![
            doc! {
                "$project": {
                    "_id": 0,
                    "id": 1,
                    "author": {
                        "id": "$author.id",
                        "icon": "$author.icon",
                        "displayName": "$author.displayName",
                        "username": "$author.username",
                        "roles": "$author.roles",
                        "ratingAvg": {
                            "$cond": {
                                "if": { "$eq": ["$ratingCount", 0] },
                                "then": 0,
                                "else": { "$divide": ["$ratingSum", "$ratingCount"] }
                            }
                        }
                    },
                    "title": 1,
                    "ratingAvg": {
                        "$cond": {
                            "if": { "$eq": ["$ratingCount", 0] },
                            "then": 0,
                            "else": { "$divide": ["$ratingSum", "$ratingCount"] }
                        }
                    },
                    "description": { "$substrCP": ["$description", 0, 100] },
                    "prepTime": 1,
                    "allergens": 1,
                    "tags": 1,
                    "thumbnail": 1,
                    "viewCount": 1
                }
            },
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
        ]);

        let mut cursor = self.collection.aggregate(pipeline, None).await?;
        if let Some(document) = cursor.try_next().await? {
            let response: AggregationResponse<Recipe> = from_document(document)?;
            return Ok(response);
        };

        Ok(AggregationResponse::default())
    }
}
