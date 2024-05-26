FROM rust:1.76.0-slim-buster 

WORKDIR /app

COPY ./ ./

RUN apt update --quiet --assume-yes && \
    apt upgrade --quiet --assume-yes && \
    apt install pkg-config libssl-dev --quiet --assume-yes && \
    cargo install cargo-watch && \
    cargo build --release

# CMD ["./target/release/search_cooking_app"]
CMD cargo watch -x run
