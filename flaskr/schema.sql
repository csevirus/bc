DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS problem;
DROP TABLE IF EXISTS submission;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  gender TEXT NOT NULL,
  contact TEXT NOT NULL,
  isAdmin TEXT NOT NULL DEFAULT FALSE,
  password TEXT NOT NULL
);

CREATE TABLE problem (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  title TEXT NOT NULL UNIQUE,
  body TEXT NOT NULL,
  visible TEXT NOT NULL DEFAULT FALSE,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE submission (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  problem_id INTEGER NOT NULL,
  verdict TEXT NOT NULL,
  score INTEGER NOT NULL,
  code TEXT NOT NULL,
  msg TEXT NOT NULL,
  passed INTEGER NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (problem_id) REFERENCES problem (id)
);
