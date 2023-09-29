DELETE FROM team;
DELETE FROM fixture;

INSERT INTO team(name, town, website) VALUES('Fulham', 'London', 'https://www.fulhamfc.com/');
INSERT INTO team(name, town, website) VALUES('Manchester United', 'Manchester', NULL);
INSERT INTO team(name, town, website) VALUES('Arsenal', 'London', NULL);
INSERT INTO team(name, town, website) VALUES('Manchester City', 'Manchester', NULL);
INSERT INTO team(name, town, website) VALUES('Luton', 'Luton', NULL);
INSERT INTO team(name, town, website) VALUES('Everton', 'Liverpool', NULL);
INSERT INTO team(name, town, website) VALUES('Brentford', 'London', NULL);
INSERT INTO team(name, town, website) VALUES('Crystal Palace', 'London', NULL);
INSERT INTO team(name, town, website) VALUES('Chelsea', 'London', NULL);
INSERT INTO team(name, town, website) VALUES('Sheffield United', 'Sheffield', NULL);
INSERT INTO team(name, town, website) VALUES('Tottenham', 'London', NULL);


INSERT INTO fixture(hometeam_fk, awayteam_fk, fixturedttm) VALUES(
    (SELECT id FROM team WHERE name = 'Everton'),
    (SELECT id FROM team WHERE name = 'Fulham'),
    '2023-08-12 15:00:00');
INSERT INTO fixture(hometeam_fk, awayteam_fk, fixturedttm) VALUES(
    (SELECT id FROM team WHERE name = 'Fulham'),
    (SELECT id FROM team WHERE name = 'Brentford'),
    '2023-08-19 15:00:00');
 INSERT INTO fixture(hometeam_fk, awayteam_fk, fixturedttm) VALUES(
    (SELECT id FROM team WHERE name = 'Arsenal'),
    (SELECT id FROM team WHERE name = 'Fulham'),
    '2023-08-26 15:00:00');
 INSERT INTO fixture(hometeam_fk, awayteam_fk, fixturedttm) VALUES(
    (SELECT id FROM team WHERE name = 'Manchester City'),
    (SELECT id FROM team WHERE name = 'Fulham'),
    '2023-09-02 15:00:00');
 INSERT INTO fixture(hometeam_fk, awayteam_fk, fixturedttm) VALUES(
    (SELECT id FROM team WHERE name = 'Fulham'),
    (SELECT id FROM team WHERE name = 'Luton'),
    '2023-09-16 15:00:00');
