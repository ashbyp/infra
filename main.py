import datetime
import functools
import yaml

from typing import Any
from dataclasses import asdict

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api import football, system

#########################
# Startup
#########################
app = FastAPI()
app.mount("/static", StaticFiles(directory="site/static"), name="static")
templates = Jinja2Templates(directory="site/templates")


#########################
# APIS
#########################

def load_settings() -> dict[Any, Any]:
    with open('settings.yaml') as file:
        return yaml.safe_load(file)


@functools.cache
def football_api() -> football.FootballAPI:
    settings = load_settings()
    return football.FootballAPI(settings['pgsql-dev'])


@functools.cache
def system_api() -> system.SystemAPI:
    return system.SystemAPI()


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
    return Response(f'API server is alive: {datetime.datetime.now()}')


@app.get("/status", response_class=HTMLResponse)
def get_status(request: Request) -> Response:
    status = system_api().get_status()
    status['request'] = request
    return templates.TemplateResponse("status.html", status)


#########################
# Football Endpoints
#########################
@app.get("/teams", response_class=HTMLResponse)
def get_teams(request: Request) -> Response:
    data = {
        'request': request,
        'teams': [asdict(t) for t in football_api().get_teams()]
    }
    return templates.TemplateResponse('teams.html', data)


@app.get("/matches", response_class=HTMLResponse)
def get_matches(request: Request) -> Response:
    data = {
        'request': request,
        'matches': [asdict(t) for t in football_api().get_matches()]
    }
    return templates.TemplateResponse('matches.html', data)


@app.get("/data/teams", response_model=list[football.Team])
def get_teams() -> list[football.Team]:
    return football_api().get_teams()


@app.get("/data/matches", response_model=list[football.Match])
def get_matches() -> list[football.Match]:
    return football_api().get_matches()
