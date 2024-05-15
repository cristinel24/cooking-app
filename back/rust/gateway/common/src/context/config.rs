use anyhow::{ensure, Result};
use clap::Parser;
use figment::{
    providers::{Env, Format, Json, Serialized},
    Figment,
};
use models::context::config::{CommandLineArguments, Configuration};

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
