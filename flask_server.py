import secrets

from flask import Flask, request, g

from bot import Bot
from interfaces.logger import Logger
from interfaces.market_data import MarketData
from interfaces.repository.in_memory import Repository
from interfaces.web_app import WebApp

app = Flask(__name__)
secret = secrets.token_urlsafe(32)
app.secret_key = secret


bot = None


@app.route("/init", methods=["POST"])
def initialize():
    global bot
    bot = Bot(
        web_app=WebApp(headless=False),
        logger=Logger(),
        repository=Repository(),
        market_data=MarketData(),
    )
    return "Session initialized"


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    response = bot.login(username=data["username"], password=data["password"])
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


# TODO Hier sessie maken


@app.route("/mass-bid", methods=["POST"])
def mass_bid():
    data = request.get_json()
    response = bot.mass_bid(
        platform=data["platform"],
        number_of_repetitions=int(data["number_of_repetitions"]),
        max_time_left=25,
    )
    # TODO: Hier sessie beeindigen
    return "Done"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=4000)
