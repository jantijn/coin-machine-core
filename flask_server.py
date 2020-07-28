from flask import Flask, request
from webdriver_manager.chrome import ChromeDriverManager

from bots.snipe_bot import snipe_bot
  
app = Flask(__name__)

@app.route("/", methods=['POST']) 
def run():
	data = request.get_json(silent=True)
	snipe_bot.run(
		username=data.get_request('username'),
		password=data.get_request('password'),
		session_hash=data.get_request('session_hash'),
		token=data.get_request('token')
	)
	return 'Session finished'

if __name__ == "__main__": 
	app.run(host='127.0.0.1', port=4000) 
