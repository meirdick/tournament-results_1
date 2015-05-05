-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP database tournament;
CREATE database tournament;
\c tournament;

-- create table "players"
create table players (
  id serial PRIMARY KEY,
  player_name text
);

--create the matches table
create table matches (
  match_id serial primary key,
  winner integer references players(id),
  loser integer references players(id)
);

create view wins as
  SELECT players.id, count(winner) as win_count
  FROM players left join matches
  ON players.id = winner
  GROUP BY players.id
  ORDER BY win_count DESC;

create view played as
  SELECT players.id, count(*) as played_count
  FROM players join matches
  ON players.id = winner OR players.id = loser
  GROUP BY players.id
  ORDER BY played_count DESC;

create view standings as
  SELECT played.id, played_count, win_count
  FROM played left join wins
  ON played.id = wins.id
  ORDER BY win_count DESC;
