/*
use crate::endpoints::{EndpointResponse, ErrorResponse, OkResponse};
use crate::repository::get_context;
use crate::repository::models::user::User;
use mongodb::bson::doc;
use salvo::oapi::extract::JsonBody;
use salvo::prelude::{endpoint, Json, Writer};

#[endpoint]
pub async fn test_route(user: JsonBody<User>) -> Json<EndpointResponse> {
    if let Ok(db) = get_context() {
        let test = User {
            display_name: user.display_name.clone(),
            sum_rating: user.sum_rating,
            ..Default::default()
        };

        if let Ok(e) = db
            .user_collection
            .collection
            .update_one(
                doc! { "username": "calin balan" },
                doc! {"$set": {"username": "calin balan mihai"}},
                None,
            )
            .await
        {
            println!("HELLO: {e:?}");
        };
    }

    return Json(EndpointResponse::Success(OkResponse {
        data: vec![user.display_name.clone()],
    }));
}
*/