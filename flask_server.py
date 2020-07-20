from flask import Flask, request
from webdriver_manager.chrome import ChromeDriverManager

from bots.snipe_bot import snipe_bot
  
app = Flask(__name__)

@app.route("/", methods=['POST']) 
def run():
	data = request.get_json(silent=True)
	snipe_bot.run(
		username=data.get('username'),
		password=data.get('password'),
		session_hash=data.get('session_hash'),
		token=data.get('token')
	)
	return 'Session finished'

if __name__ == "__main__": 
	app.run(host='127.0.0.1', port=4000) 
