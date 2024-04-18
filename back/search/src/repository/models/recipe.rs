use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
pub struct Recipe {
    // todo!()
}

impl Recipe {
    #[must_use]
    pub const fn get_collection_name() -> &'static str {
        "report"
    }
}
