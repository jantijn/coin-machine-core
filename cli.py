from bot import Bot
from interfaces.logger import Logger
from interfaces.market_data import MarketData
from interfaces.repository.django import Repository
from interfaces.web_app import WebApp
from use_cases.snipe_item import SnipeItem

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
    print('0) Snipe item')
    print('1) List all transfer list items')
    print('2) Run mass bid algorithm')
    print('3) Quit')
    return input('Option: ')


def list_transfer_list_items():
    bot.list_transfer_list_items()


def mass_bid():
    number_of_repetitions = input("How many reps do you want to run (1 rep is ~5 min): ")
    margin = int(input("What is the margin you want to make (compared to market price)?: "))
    bonus = int(input("For how much do you want to sell vs the market price (0 = market price)?: "))
    bot.mass_bid(
        number_of_repetitions = number_of_repetitions, margin = margin, bonus = bonus, max_time_left = 5
    )


def list_won_items():
    bonus = input("How much bonus to add to the market price: ")
    bot.list_won_items(
        margin = 200, bonus = bonus
    )


def snipe_item():
    characteristics = {}
    print('What type of search filter do you want to use?')
    print('1) Based on name')
    print('2) Based on characteristics')
    snipe_option = input('Option: ')
    if snipe_option == '1':
        type_of_filter = 'name'
        characteristics['name'] = input("What is the name of the item you want to snipe?: ")
    elif snipe_option == '2':
        type_of_filter = 'characteristics'
        characteristics['name'] = input("What is the name of the item you want to snipe?: ")
        characteristics['club'] = input("What is the club the item plays?: ")
        characteristics['nation'] = input("What is the nation of the item?: ")
        characteristics['position'] = input("What is the position of the item?: ")
    price = int(input("What is the max price you want to pay?: "))
    number_of_attempts = int(input("How many attempts do you want to do?: "))

    bot.snipe_item(
        characteristics = characteristics,
        price = price,
        number_of_attempts = number_of_attempts,
        type_of_filter = type_of_filter
    )


if __name__ == "__main__":
    login()
    login_to_webapp()
    verify_device()
    while True:
        option = select_option()
        if option == "0":
            snipe_item()
        if option == "1":
            list_transfer_list_items()
        elif option == "2":
            mass_bid()
        elif option == "3":
            break

