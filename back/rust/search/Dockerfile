FROM rust:1.76.0-slim-buster 

WORKDIR /search-service

COPY ./ ./

RUN apt update --quiet --assume-yes \
    && apt upgrade --quiet --assume-yes \ 
    && cargo build --release

CMD ["./target/release/search_cooking_app"]
