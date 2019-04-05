-- Competition [ent3]
create table `competition` (
   `oid`  integer  not null,
  primary key (`oid`)
);


-- Team [ent4]
create table `team` (
   `oid`  integer  not null,
  primary key (`oid`)
);


-- Event [ent2]
alter table `event`  add column  `type`  integer;


-- Team_Event [rel2]
alter table `team`  add column  `event_oid`  integer;
alter table `team`   add index fk_team_event (`event_oid`), add constraint fk_team_event foreign key (`event_oid`) references `event` (`oid`);


-- Event_Competition [rel3]
alter table `event`  add column  `competition_oid`  integer;
alter table `event`   add index fk_event_competition (`competition_oid`), add constraint fk_event_competition foreign key (`competition_oid`) references `competition` (`oid`);


-- Event_Team [rel4]
alter table `team`  add column  `event_oid_2`  integer;
alter table `team`   add index fk_team_event_2 (`event_oid_2`), add constraint fk_team_event_2 foreign key (`event_oid_2`) references `event` (`oid`);


-- Team_Competition [rel5]
create table `team_competition` (
   `team_oid`  integer not null,
   `competition_oid`  integer not null,
  primary key (`team_oid`, `competition_oid`)
);
alter table `team_competition`   add index fk_team_competition_team (`team_oid`), add constraint fk_team_competition_team foreign key (`team_oid`) references `team` (`oid`);
alter table `team_competition`   add index fk_team_competition_competitio (`competition_oid`), add constraint fk_team_competition_competitio foreign key (`competition_oid`) references `competition` (`oid`);


-- Bet_Event [rel6]
alter table `event`  add column  `bet_result`  integer;
alter table `event`   add index fk_event_bet (`bet_result`), add constraint fk_event_bet foreign key (`bet_result`) references `bet` (`result`);


