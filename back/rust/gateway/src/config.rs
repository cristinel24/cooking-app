use anyhow::{ensure, Result};
use clap::{Parser, ValueHint};
use figment::{
    providers::{Env, Format, Json, Serialized},
    Figment,
};
use once_cell::sync::OnceCell;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::PathBuf;

#[derive(Debug, Serialize, Deserialize)]
pub struct InputData {
    pub host: String,
    pub port: usize,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Route {
    pub source: String,
    pub target: String,
    pub auth: Option<bool>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Service {
    pub url: String,
    pub port: u16,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Configuration {
    pub context: String,
    pub input: InputData,
    pub services: HashMap<String, Service>,
}

#[derive(Debug, Parser, Serialize, Default)]
pub struct CommandLineArguments {
    #[arg(short = 'c', long = "config_filepath")]
    #[clap(value_parser, value_hint = ValueHint::FilePath, default_value = "config.json")]
    pub config_filepath: PathBuf,
}

/// # Errors
/// * Configuration file does not exist!
/// * Bad configuration file!
pub fn get_configuration() -> Result<Configuration> {
    let cmd_args = Serialized::defaults(CommandLineArguments::parse());
    let config_file = &cmd_args.value.config_filepath;
    ensure!(
        config_file.exists(),
        "Configuration file <{}> does not exist!",
        config_file.display().to_string()
    );

    Ok(Figment::new()
        .merge(Json::file(config_file.clone()))
        .merge(Env::prefixed("Cooking-APP_"))
        .merge(cmd_args)
        .extract()?)
}

pub static CONTEXT: OnceCell<Configuration> = OnceCell::new();

/// # Errors
/// * Couldn't load `CookingApp` Configuration
#[inline]
pub fn get_global_context() -> Result<&'static Configuration> {
    CONTEXT.get().map_or_else(
        || Err(anyhow::Error::msg("Couldn't load CookingApp Configuration")),
        Ok,
    )
}
