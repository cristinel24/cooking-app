use clap::{Parser, ValueHint};
use serde::{Deserialize, Serialize};
use std::path::PathBuf;

#[derive(Debug, Serialize, Deserialize)]
pub struct InputData {
    pub host: String,
    pub port: usize,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Services {
    pub register_service: Service,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Service {
    pub url: String,
    pub port: usize,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Configuration {
    pub context: String,
    pub input: InputData,
    pub services: Services,
}

#[derive(Debug, Parser, Serialize, Default)]
pub struct CommandLineArguments {
    #[arg(short = 'c', long = "config_filepath")]
    #[clap(value_parser, value_hint = ValueHint::FilePath, default_value = "config.json")]
    pub config_filepath: PathBuf,
}
