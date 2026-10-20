import heapq
import json
import os
import random
import secrets
import string
import threading
import time
import urllib.request

MAX_PLAYERS = 25
DURATIONS = {60, 300}
COUNTDOWN = 5
TTL = 7200
CODE_CHARS = string.ascii_uppercase + string.digits
BOT_NAMES = ["Bot Ada", "Bot Linus", "Bot Grace", "Bot Alan"]


class GameError(Exception):
    def __init__(self, msg, status=400):
        super().__init__(msg)
        self.msg = msg
        self.status = status


class MemoryStore:
    def __init__(self):
        self.d = {}
        self.lock = threading.Lock()

    def create(self, code, meta):
        with self.lock:
            if code in self.d:
                return False
            self.d[code] = {"meta": meta, "scores": {}, "times": {}}
            return True

    def set_meta(self, code, meta):
        with self.lock:
            self.d[code]["meta"] = meta

    def add(self, code, name):
        with self.lock:
            r = self.d[code]
            if name in r["scores"]:
                return "taken"
            if len(r["scores"]) >= MAX_PLAYERS:
                return "full"
            r["scores"][name] = 0
            r["times"][name] = 0.0
            return "ok"

    def incr(self, code, name, n):
        with self.lock:
            r = self.d[code]
            if name in r["scores"]:
                r["scores"][name] += n
                r["times"][name] = time.time()

    def reset(self, code):
        with self.lock:
            r = self.d[code]
            for k in r["scores"]:
                r["scores"][k] = 0
                r["times"][k] = 0.0

    def snap(self, code):
        with self.lock:
            r = self.d.get(code)
            if not r:
                return None
            return dict(r["meta"]), dict(r["scores"]), dict(r["times"])


class RedisStore:
    def __init__(self, url, token):
        self.url = url.rstrip("/")
        self.token = token

    def run(self, *cmds):
        req = urllib.request.Request(
            self.url + "/pipeline",
            data=json.dumps(list(cmds)).encode(),
            headers={"Authorization": "Bearer " + self.token, "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=6) as r:
            return [x.get("result") for x in json.load(r)]

    @staticmethod
    def keys(code):
        return f"r:{code}:m", f"r:{code}:s", f"r:{code}:t"

    def create(self, code, meta):
        m, _, _ = self.keys(code)
        return self.run(["SET", m, json.dumps(meta), "NX", "EX", str(TTL)])[0] == "OK"

    def set_meta(self, code, meta):
        m, _, _ = self.keys(code)
        self.run(["SET", m, json.dumps(meta), "EX", str(TTL)])

    def add(self, code, name):
        _, s, t = self.keys(code)
        if self.run(["HSETNX", s, name, "0"])[0] == 0:
            return "taken"
        self.run(["HSET", t, name, "0"], ["EXPIRE", s, str(TTL)], ["EXPIRE", t, str(TTL)])
        if self.run(["HLEN", s])[0] > MAX_PLAYERS:
            self.run(["HDEL", s, name], ["HDEL", t, name])
            return "full"
        return "ok"

    def incr(self, code, name, n):
        _, s, t = self.keys(code)
        self.run(["HINCRBY", s, name, str(n)], ["HSET", t, name, str(time.time())])

    def reset(self, code):
        _, s, t = self.keys(code)
        names = self.run(["HKEYS", s])[0] or []
        if names:
            flat = [x for n in names for x in (n, "0")]
            self.run(["HSET", s, *flat], ["HSET", t, *flat])

    def snap(self, code):
        m, s, t = self.keys(code)
        mj, sl, tl = self.run(["GET", m], ["HGETALL", s], ["HGETALL", t])
        if not mj:
            return None
        sl, tl = sl or [], tl or []
        scores = {k: int(v) for k, v in zip(sl[::2], sl[1::2])}
        times = {k: float(v) for k, v in zip(tl[::2], tl[1::2])}
        return json.loads(mj), scores, times


def make_store():
    url = os.environ.get("UPSTASH_REDIS_REST_URL") or os.environ.get("KV_REST_API_URL")
    tok = os.environ.get("UPSTASH_REDIS_REST_TOKEN") or os.environ.get("KV_REST_API_TOKEN")
    return RedisStore(url, tok) if url and tok else MemoryStore()


store = make_store()


def ranking(scores, times):
    heap = [(-s, times.get(n, 0.0), n) for n, s in scores.items()]
    heapq.heapify(heap)
    order = []
    while heap:
        neg, _, n = heapq.heappop(heap)
        order.append((n, -neg))
    return order


def status(meta, now):
    if not meta["start_at"]:
        return "lobby"
    if now < meta["start_at"]:
        return "countdown"
    if now < meta["end_at"]:
        return "playing"
    return "finished"


def bot_state(meta, now):
    bots = meta.get("bots") or {}
    if not meta["start_at"]:
        return {n: 0 for n in bots}, {n: 0.0 for n in bots}
    elapsed = max(0.0, min(now, meta["end_at"]) - meta["start_at"])
    whole = int(elapsed)
    scores, times = {}, {}
    for n, rate in bots.items():
        rng = random.Random(f"{n}:{int(meta['start_at'])}")
        total = sum(rng.uniform(0.5, 1.5) * rate for _ in range(whole))
        total += rng.uniform(0.5, 1.5) * rate * (elapsed - whole)
        scores[n] = int(total)
        times[n] = meta["start_at"] + elapsed
    return scores, times


def build(meta, scores, times, name, now):
    bs, bt = bot_state(meta, now)
    humans = list(scores)
    scores = {**scores, **bs}
    times = {**times, **bt}
    order = ranking(scores, times)
    rank = {n: i + 1 for i, (n, _) in enumerate(order)}
    st = status(meta, now)
    winner = None
    if st == "finished" and order:
        winner = {"name": order[0][0], "score": order[0][1]}
    return {
        "status": st,
        "now": now,
        "start_at": meta["start_at"],
        "end_at": meta["end_at"],
        "duration": meta["duration"],
        "host": meta["host"],
        "players": humans + list(bs),
        "solo": bool(meta.get("solo")),
        "top": [{"name": n, "score": s} for n, s in order[:10]],
        "me": {"rank": rank.get(name), "score": scores.get(name, 0)},
        "winner": winner,
    }


def create_room(name, solo=False):
    token = secrets.token_hex(8)
    if solo and name in BOT_NAMES:
        raise GameError("Choose another name")
    bots = {n: round(random.uniform(2.0, 6.0), 2) for n in BOT_NAMES} if solo else {}
    for _ in range(30):
        code = "".join(random.choices(CODE_CHARS, k=5))
        meta = {"host": name, "token": token, "duration": 60, "start_at": 0, "end_at": 0, "solo": solo, "bots": bots}
        if store.create(code, meta):
            store.add(code, name)
            return code, token
    raise GameError("Try again", 503)


def join_room(code, name):
    snap = store.snap(code)
    if not snap:
        raise GameError("Room not found", 404)
    if snap[0].get("solo"):
        raise GameError("Solo room", 409)
    if status(snap[0], time.time()) in ("countdown", "playing"):
        raise GameError("Game already started", 409)
    res = store.add(code, name)
    if res == "taken":
        raise GameError("Name already taken", 409)
    if res == "full":
        raise GameError(f"Room full ({MAX_PLAYERS})", 409)


def start_room(code, token, duration):
    snap = store.snap(code)
    if not snap:
        raise GameError("Room not found", 404)
    meta = snap[0]
    if meta["token"] != token:
        raise GameError("Only the host can start", 403)
    if duration not in DURATIONS:
        raise GameError("Invalid duration")
    now = time.time()
    if status(meta, now) in ("countdown", "playing"):
        raise GameError("Game in progress", 409)
    store.reset(code)
    meta["duration"] = duration
    meta["start_at"] = now + COUNTDOWN
    meta["end_at"] = meta["start_at"] + duration
    store.set_meta(code, meta)


def sync(code, name, clicks):
    snap = store.snap(code)
    if not snap:
        raise GameError("Room not found", 404)
    meta, scores, times = snap
    if name not in scores:
        raise GameError("Not in room", 403)
    now = time.time()
    if status(meta, now) == "playing" or (meta["end_at"] and meta["end_at"] <= now < meta["end_at"] + 1):
        n = max(0, min(int(clicks or 0), 30))
        if n and meta["start_at"] <= now:
            store.incr(code, name, n)
            scores[name] += n
            times[name] = now
    out = build(meta, scores, times, name, now)
    return out
