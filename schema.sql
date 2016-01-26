drop table if exists prices;
create table prices (
  id integer primary key autoincrement,
  name text not null,
  factor float not null,
  updated_at timestamp
);