from bot import Bot
from interfaces.logger import Logger
from interfaces.market_data import MarketData
from interfaces.repository.django import Repository
from interfaces.web_app import WebApp

bot = Bot(
    web_app = WebApp(headless = True),
    logger = Logger(),
    repository = Repository(),
    market_data = MarketData()
)


def login():
    try:
        _login()
    except:
        login()

def _login():
    print('Enter your CoinMachine credentials')

    username = input('Username: ')
    password = input('Password: ')

    bot.repository.login(
        username = username, password = password
    )

    print('Login successful!')


def login_to_webapp():
    try:
        _login_to_webapp()
    except:
        login_to_webapp()


def _login_to_webapp():
    print('Enter your EA credentials')

    bot.username = input('Username: ')
    bot.password = input('Password: ')

    response = bot.login()
    if response:
        print("Successful login!")
    else:
        raise Exception("Something went wrong")


if __name__ == "__main__":
    login()
    login_to_webapp()
