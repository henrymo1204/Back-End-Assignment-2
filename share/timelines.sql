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
    usernameToFollow VARCHAR
);
INSERT INTO posts(username, text, time) VALUES('henry', 'Hi, I am Henry.', '2021-03-07 23:25:32');
INSERT INTO posts(username, text, time) VALUES('henry', 'Testing, testing, does this app works?', '2021-03-07 23:26:32');
INSERT INTO posts(username, text, time) VALUES('calvin', 'Yes, it works', '2021-03-07 23:27:32');
INSERT INTO posts(username, text, time) VALUES('tommy', 'Yes, this app works.', '2021-03-07 23:28:32');
INSERT INTO posts(username, text, time) VALUES('calvin', 'TEST', '2021-03-07 23:29:32');
INSERT INTO followers(username, usernameToFollow) VALUES('henry', 'calvin');
INSERT INTO followers(username, usernameToFollow) VALUES('henry', 'tommy');
INSERT INTO followers(username, usernameToFollow) VALUES('calvin', 'henry');
INSERT INTO followers(username, usernameToFollow) VALUES('tommy', 'henry');
COMMIT;
