-- $ sqlite3 timelines.db < timelines.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS followers;
CREATE TABLE posts (
    id INTEGER primary key,
    username VARCHAR,
    text VARCHAR,
    time TIMESTAMP
);
CREATE TABLE followers (
    id INTEGER primary key,
    username VARCHAR,
    usernameToFollow VARCHAR,
    FOREIGN KEY(username) REFERENCES posts(username)
);
COMMIT;
