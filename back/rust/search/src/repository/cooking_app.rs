use crate::repository::service::{allergen, recipe, tag, user, DATABASE_NAME};
use anyhow::Result;
use mongodb::options::{ClientOptions, ConnectionString, ReadPreference, ReadPreferenceOptions};
use mongodb::Client;

pub struct CookingAppRepository {
    pub user_collection: user::Service,
    pub recipe_collection: recipe::Service,
    pub tag_collection: tag::Service,
    pub allergen_collection: allergen::Service,
}

impl CookingAppRepository {
    pub async fn new(url: &str) -> Result<Self> {
        let client = Self::new_client(url).await?;

        Ok(Self {
            user_collection: user::Service::new(&client),
            recipe_collection: recipe::Service::new(&client),
            tag_collection: tag::Service::new(&client),
            allergen_collection: allergen::Service::new(&client),
        })
    }

    async fn new_client(url: &str) -> Result<Client> {
        let mut connection_string = ConnectionString::parse(url)?;

        connection_string.read_preference = Some(ReadPreference::Secondary {
            options: ReadPreferenceOptions::default(),
        });

        connection_string.app_name = Some(DATABASE_NAME.to_string());

        let options = ClientOptions::parse_connection_string(connection_string).await?;
        let client = Client::with_options(options)?;
        Ok(client)
    }
}
