import datetime
import functools
import yaml

from typing import Any, Annotated
from dataclasses import asdict

from fastapi import FastAPI, Request, Response, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api import football, system, stash
from api.API import API

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
def inmem_api() -> stash.StashAPI:
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
def home(request: Request) -> Response:
    data = {
        'request': request,
        'routes': [{"path": route.path, "name": route.name} for route in request.app.routes]
    }
    return templates.TemplateResponse('routes.html', data)


@app.get("/ping")
def ping() -> Response:
    apis = [(a.name(), a.ping()) for a in (system_api(), football_api(), inmem_api())]
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


@app.get("/matches", response_class=HTMLResponse)
def matches(request: Request) -> Response:
    data = {
        'request': request,
        'matches': [asdict(t) for t in football_api().get_matches()]
    }
    return templates.TemplateResponse('matches.html', data)


@app.get("/data/teams", response_model=list[football.Team])
def data_teams(_request: Request) -> list[football.Team]:
    return football_api().get_teams()


@app.get("/data/matches", response_model=list[football.Match])
def data_matches(_request: Request) -> list[football.Match]:
    return football_api().get_matches()


@app.post("/create-team/", response_class=HTMLResponse)
def create_team(request: Request, team: Annotated[str, Form()], town: Annotated[str, Form()]) -> Response:
    if not (team and town):
        message = "Missing team or town, please try again"
    else:
        message = football_api().create_or_update_team(football.Team(team, town))
    return _render_teams_page(request, message)


def _render_teams_page(request: Request, message: str) -> Response:
    data = {
        'request': request,
        'message': message,
        'teams': [asdict(t) for t in football_api().get_teams()]
    }
    return templates.TemplateResponse('teams.html', data)
