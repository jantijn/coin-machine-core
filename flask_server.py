import secrets

from flask import Flask, request, g

from bot import Bot
from interfaces.logger import Logger
from interfaces.market_data import MarketData
from interfaces.repository.django import Repository
from interfaces.web_app import WebApp

app = Flask(__name__)
secret = secrets.token_urlsafe(32)
app.secret_key = secret


bot = None


@app.route("/init", methods=["POST"])
def initialize():
    data = request.get_json()
    global bot
    bot = Bot(
        web_app=WebApp(headless=True),
        logger=Logger(),
        repository=Repository(),
        market_data=MarketData()
    )
    bot.repository.login(
        username = data["username"], password = data["password"]
    )
    return "Session initialized"


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    bot.username = data["username"]
    bot.password = data["password"]
    response = bot.login()
    if response:
        return "Successful login!"
    return "Something went wrong"


@app.route("/verify-device", methods=["POST"])
def verify_device():
    data = request.get_json()
    response = bot.verify_device(verification_code=data["verification_code"],)
    if response:
        return "Successfully verified device!"
    return "Something went wrong"


@app.route("/create-session", methods=["POST"])
def create_session():
    session = bot.repository.create_session()
    return session


@app.route("/mass-bid", methods=["POST"])
def mass_bid():
    data = request.get_json()
    response = bot.mass_bid(
        platform=data["platform"],
        number_of_repetitions=int(data["number_of_repetitions"]),
        max_time_left=25,
    )
    bot.repository.stop_session()
    return "Done"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=4000)
