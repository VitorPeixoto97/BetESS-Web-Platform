-- Bet [ent1]
alter table `bet`  add column  `oid`  integer  not null;


-- Event [ent2]
alter table `event`  add column  `oddv`  double precision;
alter table `event`  add column  `odde`  double precision;
alter table `event`  add column  `oddd`  double precision;
alter table `event`  add column  `status`  bit;
alter table `event`  add column  `result`  integer;


-- Competition [ent3]
alter table `competition`  add column  `name`  varchar(255);
alter table `competition`  add column  `country`  varchar(255);


-- Team [ent4]
alter table `team`  add column  `name`  varchar(255);
alter table `team`  add column  `simbolo`  varchar(255);


