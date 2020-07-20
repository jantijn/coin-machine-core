from factories.use_case_factory import build_login

class LoginBot:
	def __init__ (self):
		pass

	def run(self, driver, username, password):
		login = build_login(driver)

		try:
			login(
				username = username,
				password = password
			)
		except:
			pass
		return driver

login_bot = LoginBot()