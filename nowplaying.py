#!/usr/bin/python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
from flask import Flask, request
import pylast
import json
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
# username = os.environ..get("USERNAME")
PASS_HASH = pylast.md5(os.environ.get("PASS_HASH"))
USERNAME = ""

network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=USERNAME,
    password_hash=PASS_HASH,
)

app = Flask(__name__)


def now_playing(username):
    np = network.get_user(username).get_now_playing()
    return np


def cover_image(username):
    cover = network.get_user(username).get_now_playing().get_cover_image()
    return cover


# duration in miliseconds
def track_duration(username):
    duration = network.get_user(username).get_now_playing().get_duration()
    return duration


def get_data(username):
    data = {
        "now_playing": str(now_playing(username)),
        "cover_image": str(cover_image(username)),
        "track_duration": str(track_duration(username)),
    }
    return json.dumps(data)


@app.route("/nowplaying")
def nowplaying():
    return get_data()


@app.route('/nowplaying/<username>')
def nowplaying_by_user(username):
    return get_data(username)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
