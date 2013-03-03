SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+0:00";
ALTER DATABASE CHARACTER SET "utf8";

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    avatar VARCHAR (128) NOT NULL DEFAULT 'http://tp1.sinaimg.cn/1377583044/180/5635933302/1',
    nickname VARCHAR(128) NOT NULL UNIQUE,
    email VARCHAR(128) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    gender tinyint NOT NULL DEFAULT 0,
    created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS notes;
CREATE TABLE notes (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    author_id VARCHAR(25) NOT NULL REFERENCES users(id),
    slug VARCHAR(100) NOT NULL UNIQUE,
    title VARCHAR(512) NOT NULL,
    content MEDIUMTEXT NOT NULL,
    created DATETIME NOT NULL,
    updated TIMESTAMP NOT NULL,
    KEY (author_id, created)
);

DROP TABLE IF EXISTS comments;
CREATE TABLE comments (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,
    parent_id INT NOT NULL DEFAULT 0,
    user_id VARCHAR (25) NOT NULL REFERENCES users(id),
    note_id VARCHAR (25) NOT NULL REFERENCES notes(id),
    content VARCHAR (1024) NOT NULL,
    created DATETIME NOT NULL,
    key (user_id,created)
);