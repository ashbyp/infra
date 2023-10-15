from dataclasses import dataclass, field
from typing import Any
from datetime import datetime

import psycopg2
import psycopg2.extras

from api.API import API


@dataclass(order=True)
class Team:
    sort_index: str = field(init=False, repr=False)

    name: str
    town: str
    website: str

    def __post_init__(self):
        self.sort_index = self.name


@dataclass
class Fixture:
    home_team: str
    away_team: str
    dttm: datetime


class FootballAPI(API):

    def __init__(self, db_config: dict[Any, Any]) -> None:
        super().__init__()
        self._con = psycopg2.connect(
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port']
        )

    def ping(self) -> str:
        cur = self._con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("select 'hello' as test")
        results = cur.fetchall()
        cur.close()
        super().called()
        return 'OK'

    def get_teams(self) -> list[Team]:
        cur = self._con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("select name, town, website from team")
        results = [Team(**r) for r in cur.fetchall()]
        cur.close()
        super().called()
        return results

    def get_team(self, name: str) -> Team:
        cur = self._con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(f"select name, town, website from team where name = '{name}'")
        results = [Team(**r) for r in cur.fetchall()]
        cur.close()
        super().called()
        return results[0] if results else None

    def delete_team(self, name: str) -> str:
        cur = self._con.cursor()
        try:
            cur.execute("delete from team where name = %s", (name,))
            self._con.commit()
        except Exception as e:
            self._con.rollback()
            return f'failed to delete team {name} {e}'
        finally:
            cur.close()
            super().called()
        return f'deleted team {name}'

    def delete_fixture(self, home: str, away: str) -> str:
        cur = self._con.cursor()
        try:
            query = """
            delete from fixture
            where hometeam_fk = (select id from team where name = %s)
            and awayteam_fk = (select id from team where name= %s)
            """
            cur.execute(query, (home, away))
            self._con.commit()
        except Exception as e:
            self._con.rollback()
            return f'failed to delete fixture {home} vs. {away} {e}'
        finally:
            cur.close()
            super().called()
        return f'deleted fixture {home} vs. {away}'

    def get_fixtures(self) -> list[Fixture]:
        cur = self._con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            """
            select h.name as home_team, 
                    a.name as away_team, 
                    f.fixturedttm as dttm
            from fixture f 
            join team h on h.id = f.hometeam_fk 
            join team a on a.id = f.awayteam_fk
            """)

        results = [Fixture(**r) for r in cur.fetchall()]
        cur.close()
        super().called()
        return results

    def get_fixture(self, home_team: str, away_team: str) -> Fixture:
        cur = self._con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            """
            select h.name as home_team, 
                    a.name as away_team, 
                    f.fixturedttm as dttm
            from fixture f 
            join team h on h.id = f.hometeam_fk 
            join team a on a.id = f.awayteam_fk
            where h.name = %s and a.name = %s
            """, (home_team, away_team))

        results = [Fixture(**r) for r in cur.fetchall()]
        cur.close()
        super().called()
        return results[0] if results else None

    def create_team(self, team: Team) -> str:
        cur = self._con.cursor()
        try:
            cur.execute("insert into team(name, town, website) VALUES (%s, %s, %s)",
                        (team.name, team.town, team.website))
            self._con.commit()
        except Exception as e:
            self._con.rollback()
            return f'failed to add team {team} {e}'
        finally:
            cur.close()
            super().called()
        return f'added team {team}'

    def update_team(self, team: Team) -> str:
        cur = self._con.cursor()
        try:
            cur.execute(f"update team set town = %s, website = %s where name = %s",
                        (team.town, team.website, team.name))
            self._con.commit()
        except Exception as e:
            self._con.rollback()
            return f'failed to update team {team} {e}'
        finally:
            cur.close()
            super().called()
        return f'updated team {team}'

    def create_or_update_team(self, team: Team) -> str:
        existing = self.get_team(team.name)
        if existing:
            return self.update_team(team)
        else:
            return self.create_team(team)

    def create_fixture(self, fixture: Fixture) -> str:
        cur = self._con.cursor()
        try:
            query = """
            insert into fixture(hometeam_fk,awayteam_fk, fixturedttm)
            values ((select id from team where name = %s),
                    (select id from team where name = %s),
                    %s)
            """
            cur.execute(query, (fixture.home_team, fixture.away_team, fixture.dttm))
            self._con.commit()
        except Exception as e:
            self._con.rollback()
            return f'failed to create fixture {fixture} {e}'
        finally:
            cur.close()
            super().called()
        return f'added fixture {fixture}'

    def update_fixture(self, fixture: Fixture) -> str:
        cur = self._con.cursor()
        try:
            query = """
            update fixture AS f
                set fixturedttm = %s
            from team AS h, team AS a
            where h.id = f.hometeam_fk
            and a.id = f.awayteam_fk
            and h.name = %s
            and a.name = %s;
            """
            cur.execute(query, (fixture.dttm, fixture.home_team, fixture.away_team))
            self._con.commit()
        except Exception as e:
            self._con.rollback()
            return f'failed to create fixture {fixture} {e}'
        finally:
            cur.close()
            super().called()
        return f'added fixture {fixture}'

    def create_or_update_fixture(self, fixture: Fixture) -> str:
        existing = self.get_fixture(fixture.home_team, fixture.away_team)
        if existing:
            return self.update_fixture(fixture)
        else:
            return self.create_fixture(fixture)


if __name__ == '__main__':
    import yaml

    with open('../settings.yaml') as file:
        s = yaml.safe_load(file)
        s['pgsql-dev']['host'] = 'localhost'

    a = FootballAPI(s['pgsql-dev'])
    print(a.get_teams())
    print(a.get_fixtures())
