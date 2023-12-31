import datetime
import functools
import yaml

from typing import Any, Annotated
from dataclasses import asdict

from fastapi import FastAPI, Request, Response, Form, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api import football, system, stash
from api.API import API
from utils import dttmutils

#########################
# Startup
#########################
app = FastAPI()
app.mount("/static", StaticFiles(directory="site/static"), name="static")
templates = Jinja2Templates(directory="site/templates")
apis = []


#########################
# APIS
#########################

def load_settings() -> dict[Any, Any]:
    with open('settings.yaml') as file:
        return yaml.safe_load(file)


def register_api(api: API) -> None:
    apis.append(api)


@functools.cache
def football_api() -> football.FootballAPI:
    settings = load_settings()
    api = football.FootballAPI(settings['pgsql-dev'])
    register_api(api)
    return api


@functools.cache
def stash_api() -> stash.StashAPI:
    settings = load_settings()
    api = stash.StashAPI(settings['redis-dev'])
    register_api(api)
    return api


@functools.cache
def system_api() -> system.SystemAPI:
    api = system.SystemAPI()
    register_api(api)
    return api


#########################
# System Endpoints
#########################

@app.get("/")
def index(request: Request) -> Response:
    data = {
        'request': request,
        'routes': [{"path": route.path, "name": route.name} for route in request.app.routes]
    }
    return templates.TemplateResponse('routes.html', data)


@app.get("/ping")
def ping() -> Response:
    apis = [(a.name(), a.ping()) for a in (system_api(), football_api(), stash_api())]
    res = f'API server is alive: {datetime.datetime.now()}\n{apis}'
    return Response(res)


@app.get("/status", response_class=HTMLResponse)
def get_status(request: Request) -> Response:
    status = system_api().get_status()
    status['request'] = request
    status['apis'] = [str(api) for api in apis]
    return templates.TemplateResponse("status.html", status)


#########################
# Football Endpoints
#########################
@app.get("/teams", response_class=HTMLResponse)
def teams(request: Request) -> Response:
    return _render_teams_page(request, message="OK")


@app.get("/fixtures", response_class=HTMLResponse)
def fixtures(request: Request) -> Response:
    return _render_fixtures_page(request, "OK")


@app.get("/data/teams", response_model=list[football.Team])
def data_teams(_request: Request) -> list[football.Team]:
    return football_api().get_teams()


@app.get("/data/team/{name}", response_model=football.Team)
def data_team(_request: Request, name: str) -> football.Team:
    return football_api().get_team(name)


@app.get("/data/matches", response_model=list[football.Fixture])
def data_fixtures(_request: Request) -> list[football.Fixture]:
    return football_api().get_fixtures()


@app.post("/create-team/", response_class=HTMLResponse)
def create_team(request: Request, team: Annotated[str, Form()], town: Annotated[str, Form()],
                website: Annotated[str, Form()] = None) -> Response:
    if not team or not town:
        message = "Missing team / town, please try again"
    else:
        message = football_api().create_or_update_team(football.Team(team, town, website))
    return _render_teams_page(request, message)


@app.get("/delete-team/{name}", response_class=HTMLResponse)
def delete_team(request: Request, name: str) -> Response:
    message = football_api().delete_team(name)
    return _render_teams_page(request, message)


@app.get("/delete-fixture/{home}/{away}", response_class=HTMLResponse)
def delete_fixture(request: Request, home: str, away: str) -> Response:
    message = football_api().delete_fixture(home, away)
    return _render_fixtures_page(request, message)


@app.post("/create-fixture/", response_class=HTMLResponse)
def create_fixture(request: Request, home: Annotated[str, Form()], away: Annotated[str, Form()],
                   dttmstr: Annotated[str, Form()]) -> Response:
    if not all([home, away, dttmstr]):
        message = f"Missing fixture details {home} {away} {dttmstr}"
    elif home == away:
        message = f'{home} cannot play themselves'
    else:
        message = football_api().create_or_update_fixture(
            football.Fixture(home, away, dttmutils.to_dttm_no_minutes(dttmstr)))
    return _render_fixtures_page(request, message)


def _render_teams_page(request: Request, message: str) -> Response:
    data = {
        'request': request,
        'message': message,
        'teams': [asdict(t) for t in sorted(football_api().get_teams())]
    }
    return templates.TemplateResponse('teams.html', data)


def _render_fixtures_page(request: Request, message: str) -> Response:
    data = {
        'request': request,
        'message': message,
        'fixtures': [asdict(t) for t in football_api().get_fixtures()],
        'teams': [t.name for t in sorted(football_api().get_teams())],
        'next_saturday': dttmutils.format_dttm_no_minutes(dttmutils.next_saturday_at_3pm())
    }
    return templates.TemplateResponse('fixtures.html', data)
