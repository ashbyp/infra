import json
from dataclasses import dataclass
from fastapi import FastAPI, HTTPException, Response

app = FastAPI()


@dataclass
class Match:
    game_id: int
    home: str
    away: str


matches: dict[int, Match] = {}

with open("data/matches.json", encoding="utf8") as f:
    data = json.load(f)
    for d in data:
        match = Match(**d)
        matches[match.game_id] = match

    print(f'Loaded {len(matches)} matches')


@app.get("/")
def status() -> Response:
    return Response("Football server is alive...")


@app.get("/matches", response_model=list[Match])
def get_matches() -> list[Match]:
    return list(matches.values())


@app.get("/match/{game_id}", response_model=Match)
def get_match(game_id: int) -> Match:
    if game_id not in matches:
        raise HTTPException(status_code=494, detail="Unknown match {id}")
    return matches[game_id]

