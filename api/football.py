from dataclasses import dataclass
from typing import Any
from datetime import datetime

import psycopg2
import psycopg2.extras

from api.API import API


@dataclass
class Team:
    name: str
    town: str
    website: str


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

    def create_team(self, team: Team) -> str:
        cur = self._con.cursor()
        try:
            cur.execute(f"insert into team(name, town, website) values('{team.name}','{team.town}', '{team.website if team.website is not None else 'null'}')")
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
            cur.execute(f"update team set town = '{team.town}', website = '{team.website}' where name = '{team.name}'")
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


if __name__ == '__main__':
    import yaml

    with open('../settings.yaml') as file:
        s = yaml.safe_load(file)
        s['pgsql-dev']['host'] = 'localhost'

    a = FootballAPI(s['pgsql-dev'])
    print(a.get_teams())
    print(a.get_fixtures())
