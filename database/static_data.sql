DELETE FROM teams;
DELETE FROM matches;

INSERT INTO teams(name, town) VALUES('Fulham', 'London');
INSERT INTO teams(name, town) VALUES('Manchester United', 'Manchester');
INSERT INTO teams(name, town) VALUES('Arsenal', 'London');
INSERT INTO teams(name, town) VALUES('Manchester City', 'Manchester');
INSERT INTO teams(name, town) VALUES('Luton', 'Luton');
INSERT INTO teams(name, town) VALUES('Everton', 'Liverpool');
INSERT INTO teams(name, town) VALUES('Brentford', 'London');
INSERT INTO teams(name, town) VALUES('Crystal Palace', 'London');
INSERT INTO teams(name, town) VALUES('Chelsea', 'London');
INSERT INTO teams(name, town) VALUES('Sheffield United', 'Sheffield');
INSERT INTO teams(name, town) VALUES('Tottenham', 'London');


INSERT INTO matches(home_team_fk, away_team_fk, fixture_dt) VALUES(
    (SELECT id FROM teams WHERE name = 'Everton'),
    (SELECT id FROM teams WHERE name = 'Fulham'),
    '2023-08-12 15:00:00');
INSERT INTO matches(home_team_fk, away_team_fk, fixture_dt) VALUES(
    (SELECT id FROM teams WHERE name = 'Fulham'),
    (SELECT id FROM teams WHERE name = 'Brentford'),
    '2023-08-19 15:00:00');
 INSERT INTO matches(home_team_fk, away_team_fk, fixture_dt) VALUES(
    (SELECT id FROM teams WHERE name = 'Arsenal'),
    (SELECT id FROM teams WHERE name = 'Fulham'),
    '2023-08-26 15:00:00');
 INSERT INTO matches(home_team_fk, away_team_fk, fixture_dt) VALUES(
    (SELECT id FROM teams WHERE name = 'Manchester City'),
    (SELECT id FROM teams WHERE name = 'Fulham'),
    '2023-09-02 15:00:00');
 INSERT INTO matches(home_team_fk, away_team_fk, fixture_dt) VALUES(
    (SELECT id FROM teams WHERE name = 'Fulham'),
    (SELECT id FROM teams WHERE name = 'Luton'),
    '2023-09-16 15:00:00');
