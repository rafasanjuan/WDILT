-- MAIN TABLE FOR STORING THE CONTENT.
CREATE TABLE post (
  id int(11) NOT NULL AUTO_INCREMENT,
  timestamp datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  content varchar(256) NOT NULL,
  username varchar(20) NOT NULL,
  tags varchar(256) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `username` (`username`)
);


-- STORES USER CREDENTIALS.
CREATE TABLE user (
    username VARCHAR(20) PRIMARY KEY,
    password VARCHAR(256) NOT NULL,
    salt VARCHAR(256) NOT NULL
);