from bot import Bot
from interfaces.logger import Logger
from interfaces.market_data import MarketData
from interfaces.repository.django import Repository
from interfaces.web_app import WebApp

bot = Bot(
    web_app = WebApp(headless = False),
    logger = Logger(),
    repository = Repository(),
    market_data = MarketData()
)


def login():
    print('Enter your CoinMachine credentials')

    username = input('Username: ')
    password = input('Password: ')

    bot.repository.login(
        username = username, password = password
    )

    print('Login successful!')


def login_to_webapp():
    print('Enter your EA credentials')

    bot.username = input('Username: ')
    bot.password = input('Password: ')

    response = bot.login()
    if response:
        print("Successful login!")
    else:
        raise Exception("Something went wrong")


def verify_device():
    print('Enter the verification code')

    verification_code = input('Verification code: ')

    response = bot.verify_device(verification_code=verification_code)
    if response:
        print("Successful verification!")
    else:
        raise Exception("Something went wrong")


def select_option():
    print('What do you want to do:')
    print('1) List all transfer list items')
    print('2) Run mass bid algorithm')
    print('3) Quit')
    return input('Option: ')


def list_transfer_list_items():
    bot.list_transfer_list_items()


def mass_bid():
    number_of_repetitions = input("How many reps do you want to run (1 rep is ~30 min): ")
    bot.mass_bid(
        number_of_repetitions = number_of_repetitions, margin = 200, max_time_left = 25
    )


if __name__ == "__main__":
    login()
    login_to_webapp()
    verify_device()
    while True:
        option = select_option()
        if option == "1":
            list_transfer_list_items()
        elif option == "2":
            mass_bid()
        elif option == "3":
            break

