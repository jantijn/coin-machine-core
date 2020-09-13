from flask import Flask, request

from bot import Bot
from interfaces.purchased_items.ignore import PurchasedItems
from interfaces.random_items.in_memory import RandomItems
from interfaces.web_app.selenium import WebApp
from logger import Logger
from interfaces.market_data import MarketData

app = Flask(__name__)

web_app = WebApp(headless = False)
logger = Logger()
random_items = RandomItems()
purchased_items = PurchasedItems()
market_data = MarketData()
bot = Bot(
    web_app = web_app,
    logger = logger,
    random_items = random_items,
    purchased_items = purchased_items,
    market_data = market_data
)


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    response = bot.login(
        username=data["username"],
        password=data["password"]
    )
    if response:
        return "Successful login!"
    return "Something went wrong"


@app.route("/verify-device", methods=["POST"])
def verify_device():
    data = request.get_json()
    response = bot.verify_device(
        verification_code = data["verification_code"],
    )
    if response:
        return "Successfully verified device!"
    return "Something went wrong"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=4000)
