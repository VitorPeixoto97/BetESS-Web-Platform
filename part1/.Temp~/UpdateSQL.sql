-- Student [ent1]
create table `student` (
   `oid`  integer  not null,
   `name`  varchar(255),
   `number`  varchar(255),
  primary key (`oid`)
);


-- Course [ent2]
create table `course` (
   `oid`  integer  not null,
   `name`  varchar(255),
   `ects`  integer,
  primary key (`oid`)
);


