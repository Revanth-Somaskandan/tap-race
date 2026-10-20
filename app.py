import re

from flask import Flask, Response, jsonify, request

import game
from page import HTML

app = Flask(__name__)


def body():
    return request.get_json(silent=True) or {}


def clean(n):
    return re.sub(r"[^\w \-]", "", str(n or "")).strip()[:16]


def code_of(b):
    return str(b.get("code", "")).strip().upper()[:5]


@app.errorhandler(game.GameError)
def on_error(e):
    return jsonify(error=e.msg), e.status


@app.get("/")
def index():
    return Response(HTML, mimetype="text/html")


@app.post("/api/create")
def create():
    b = body()
    name = clean(b.get("name"))
    solo = bool(b.get("solo"))
    if not name:
        raise game.GameError("Enter a name")
    code, token = game.create_room(name, solo)
    return jsonify(code=code, token=token, name=name, solo=solo)


@app.post("/api/join")
def join():
    b = body()
    name, code = clean(b.get("name")), code_of(b)
    if not name or not code:
        raise game.GameError("Enter name and room code")
    game.join_room(code, name)
    return jsonify(code=code, name=name)


@app.post("/api/start")
def start():
    b = body()
    try:
        duration = int(b.get("duration", 0))
    except (TypeError, ValueError):
        duration = 0
    game.start_room(code_of(b), str(b.get("token", "")), duration)
    return jsonify(ok=True)


@app.post("/api/sync")
def sync():
    b = body()
    return jsonify(game.sync(code_of(b), clean(b.get("name")), b.get("clicks", 0)))


if __name__ == "__main__":
    app.run(debug=True)
