drop table if exists users;

create table users (
  userid INTEGER PRIMARY KEY AUTOINCREMENT,
  name Char(32), 
  age Integer,
  picture Blob,
  email Char(32)
);

drop table if exists search;

create table search (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user integer,
  hashtag Char(32),
  submitted DATE,
  ttl integer,
  Foreign Key (user) REFERENCES users(userid)
);
