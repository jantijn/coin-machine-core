from bots.login_bot import login_bot
from factories.use_case_factory import build_web_driver

def login(driver):
	username = input('Enter the username: ')
	password = input('Enter the passord: ')
	return login_bot.run(driver = driver, username = username, password = password)

# def verify()
# 	verification_code = input('Enter the verification code')
# 	return verificaiton_bot.run(driver=driver, verification_code=verification_code)

if __name__ == "__main__":
	driver = build_web_driver()
	driver = login(driver)

	# try:
	# 	driver = verify(driver)
	# except:
	# 	Print('Wrong verification code, try again')
	# 	driver = verify(driver)

 #    mass_bid_bot.run(driver)
   