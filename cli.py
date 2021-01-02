from bot import Bot
from interfaces.logger import Logger
from interfaces.market_data import MarketData
from interfaces.repository.django import Repository
from interfaces.web_app import WebApp

bot = Bot(
    web_app=WebApp(headless=False),
    logger=Logger(),
    repository=Repository(),
    market_data=MarketData(),
)


def login():
    print("Enter your CoinMachine credentials")

    username = input("Username: ")
    password = input("Password: ")

    bot.repository.login(username=username, password=password)

    print("Login successful!")


def login_to_webapp():
    print("Enter your EA credentials")

    bot.username = input("Username: ")
    bot.password = input("Password: ")

    response = bot.login()
    if response:
        print("Successful login!")
    else:
        raise Exception("Something went wrong")


def verify_device():
    print("Enter the verification code")

    verification_code = input("Verification code: ")

    response = bot.verify_device(verification_code=verification_code)
    if response:
        print("Successful verification!")
    else:
        raise Exception("Something went wrong")


def select_option():
    print("What do you want to do:")
    print("0) Snipe item")
    print("1) List all transfer list items")
    print("2) List expired transfer list items for market price")
    print("3) Run mass bid algorithm")
    print("4) Quit")
    return input("Option: ")


def list_transfer_list_items():
    try:
        bot.list_transfer_list_items()
    except:
        print("On of the names does not match the database")


def list_expired_transfer_list_items():
    try:
        bot.list_expired_transfer_list_items()
    except:
        print("On of the names does not match the database")


def mass_bid():
    repetitions = input(
        "How many reps do you want to run (1 rep is ~5 min): "
    )
    margin = int(
        input("What is the margin you want to make (compared to market price)?: ")
    )
    bonus = int(
        input(
            "For how much do you want to sell vs the market price (0 = market price)?: "
        )
    )
    bot.mass_bid(
        repetitions=repetitions,
        margin=margin,
        bonus=bonus
    )


def list_won_items():
    bonus = input("How much bonus to add to the market price: ")
    try:
        bot.list_won_items(margin=200, bonus=bonus)
    except:
        print("On of the names does not match the database")


def snipe_item():
    characteristics = {}
    type_of_filter = None
    print("What type of search filter do you want to use?")
    print("0) None (fill in filter in web app manually)")
    print("1) Based on name")
    print("2) Based on characteristics")
    snipe_option = input("Option: ")
    price = None
    if snipe_option == "1":
        type_of_filter = "name"
        characteristics["name"] = input(
            "What is the name of the item you want to snipe?: "
        )
        price = int(input("What is the max price you want to pay?: "))
    elif snipe_option == "2":
        type_of_filter = "characteristics"
        characteristics["name"] = input(
            "What is the name of the item you want to snipe?: "
        )
        characteristics["club"] = input("What is the club the item plays?: ")
        characteristics["nation"] = input("What is the nation of the item?: ")
        characteristics["position"] = input("What is the position of the item?: ")
        price = int(input("What is the max price you want to pay?: "))
    elif snipe_option == "0":
        type_of_filter = "none"
        price = 0
    print("What do you want to do with sniped items?")
    print("0) Send to club and break")
    print("1) Send to transfer list and continue")
    print("2) List on transfer market and continue")
    snipe_option = input("Option: ")
    if snipe_option == "0":
        success_action = "send_to_club"
    elif snipe_option == "1":
        success_action = "send_to_transfer_list"
    elif snipe_option == "2":
        success_action = "list"
        characteristics["sell_price"] = int(
            input("For what price do you want to sell?: ")
        )
    number_of_attempts = int(input("How many attempts do you want to do?: "))

    bot.snipe_item(
        characteristics=characteristics,
        price=price,
        number_of_attempts=number_of_attempts,
        type_of_filter=type_of_filter,
        success_action=success_action,
    )


if __name__ == "__main__":
    login()
    login_to_webapp()
    verify_device()
    while True:
        option = select_option()
        if option == "0":
            snipe_item()
        elif option == "1":
            list_transfer_list_items()
        elif option == "2":
            list_expired_transfer_list_items()
        elif option == "3":
            mass_bid()
        elif option == "4":
            break
