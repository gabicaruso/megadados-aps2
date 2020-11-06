USE tasklist;
DROP TABLE IF EXISTS tasks;
CREATE TABLE tasks (
    uuid BINARY(16) PRIMARY KEY,
    description NVARCHAR(1024),
    completed BOOLEAN
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    uuid BINARY(16) PRIMARY KEY,
    username NVARCHAR(1024)
);

ALTER TABLE tasks ADD user_id BINARY(16);
ALTER TABLE tasks ADD FOREIGN KEY (user_id) REFERENCES users(uuid);


