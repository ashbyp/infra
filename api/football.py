from dataclasses import dataclass
from typing import Any
from datetime import datetime

import psycopg2
import psycopg2.extras


@dataclass
class Team:
    name: str
    town: str


@dataclass
class Match:
    home_team: str
    away_team: str
    fixture: datetime


class FootballAPI:

    def __init__(self, db_config: dict[Any, Any]) -> None:
        self._con = psycopg2.connect(
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port']
        )

    def get_teams(self) -> list[Team]:
        cur = self._con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("select name, town from teams")
        results = [Team(**r) for r in cur.fetchall()]
        cur.close()
        return results

    def get_matches(self) -> list[Match]:
        cur = self._con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            """
            select h.name as home_team, 
                    a.name as away_team, 
                    m.fixture_dt as fixture 
            from matches m 
            join teams h on h.id = m.home_team_fk 
            join teams a on a.id = m.away_team_fk
            """)

        results = [Match(**r) for r in cur.fetchall()]
        cur.close()
        return results


if __name__ == '__main__':
    import yaml

    with open('../settings.yaml') as file:
        s = yaml.safe_load(file)
        s['pgsql-dev']['host'] = 'localhost'

    a = FootballAPI(s['pgsql-dev'])
    # print(a.get_teams())
    print(a.get_matches())