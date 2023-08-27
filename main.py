import functools
from typing import Any

import yaml
from fastapi import FastAPI, Response

from api import football

app = FastAPI()


def load_settings() -> dict[Any, Any]:
    with open('settings.yaml') as file:
        return yaml.safe_load(file)


@functools.cache
def football_api() -> football.FootballAPI:
    settings = load_settings()
    return football.FootballAPI(settings['pgsql-dev'])


@app.get("/")
def status() -> Response:
    return Response("Football server is alive...")


@app.get("/matches", response_model=list[football.Match])
def get_matches() -> list[football.Match]:
    return football_api().get_matches()


@app.get("/teams", response_model=list[football.Team])
def get_teams() -> list[football.Team]:
    return football_api().get_teams()
