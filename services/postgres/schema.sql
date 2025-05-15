CREATE EXTENSION postgis;
CREATE EXTENSION RUM;


\set ON_ERROR_STOP on

BEGIN;

CREATE TABLE urls (
    id_urls BIGSERIAL PRIMARY KEY,
    url TEXT 
);

CREATE TABLE users (
    id_users BIGSERIAL PRIMARY KEY,
    id_urls BIGINT REFERENCES urls(id_urls),
    screen_name TEXT,
    password TEXT
);

CREATE TABLE tweets (
    id_tweets BIGSERIAL PRIMARY KEY,
    id_users BIGINT,
    created_at TIMESTAMPTZ,
    text TEXT
);

CREATE INDEX message1 ON tweets(id_users);
CREATE INDEX message2 ON tweets(created_at);

CREATE INDEX credentials ON users(screen_name, password);

CREATE INDEX validuser ON users(screen_name);

CREATE INDEX search_tweets ON tweets USING RUM(to_tsvector('english', text));

COMMIT;
