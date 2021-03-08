-- $ sqlite3 users.db < users.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS followers;
CREATE TABLE users (
    id INTEGER primary key,
    username VARCHAR,
    password VARCHAR,
    emailAddress VARCHAR,
    UNIQUE(username, emailAddress)
);
CREATE TABLE followers (
    id INTEGER primary key,
    user_id INTEGER,
    user_id_to_follow INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(user_id_to_follow) REFERENCES users(id)
);
INSERT INTO users(username, password, emailAddress) VALUES('admin', 'admin', 'admin@gmail.com');
INSERT INTO users(username, password, emailAddress) VALUES('henry', 'henry', 'henry@gmail.com');
INSERT INTO users(username, password, emailAddress) VALUES('calvin', 'calvin', 'calvin@gmail.com');
INSERT INTO users(username, password, emailAddress) VALUES('tommy', 'tommy', 'tommy@gmail.com');
INSERT INTO users(username, password, emailAddress) 
VALUES('test', 'test', 'test@gmail.com');

/*
INSERT INTO followers(user_id, user_id_to_follow) VALUES(1, 2)
INSERT INTO followers(user_id, user_id_to_follow) VALUES(1, 3)
INSERT INTO followers(user_id, user_id_to_follow) VALUES(1, 4)
INSERT INTO followers(user_id, user_id_to_follow) VALUES(1, 5)
INSERT INTO followers(user_id, user_id_to_follow) VALUES(2, 3)
INSERT INTO followers(user_id, user_id_to_follow) VALUES(2, 4)
INSERT INTO followers(user_id, user_id_to_follow) VALUES(3, 2)
INSERT INTO followers(user_id, user_id_to_follow) VALUES(3, 4)
INSERT INTO followers(user_id, user_id_to_follow) VALUES(4, 2)
INSERT INTO followers(user_id, user_id_to_follow) VALUES(4, 3)
INSERT INTO followers(user_id, user_id_to_follow) VALUES(5, 1)
*/
COMMIT;
