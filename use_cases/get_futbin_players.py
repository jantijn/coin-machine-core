import requests
from bs4 import BeautifulSoup
import time

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6ImphbnRpam4ua3JvbXdpamtAZ21haWwuY29tIiwiZXhwIjoxNTk3MTQzOTgwLCJlbWFpbCI6ImphbnRpam4ua3JvbXdpamtAZ21haWwuY29tIn0.YJ3sUhco4FBBMH5bQBZ5t43Jhb6oIf0Z6A_Oz-bKUJM'
print("boe")

for page_number in range(1, 79):
	time.sleep(10)
	url = 'https://www.futbin.com/20/players?page=' + str(page_number) + '&version=gold'
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	players = soup.findAll("a", class_="player_name_players_table")

	for player in players:
		time.sleep(1)
		print(player)
		name = player.get_text()
		link = player['href']
		player_page = requests.get("https://www.futbin.com/" + link)
		soup = BeautifulSoup(player_page.text, 'html.parser')
		# futbin_id = soup.title.string
		img_url = soup.findAll("img", class_="lazy-main-player")[-1]['data-src']
		futbin_id = img_url.split('/')[-1].split('.')[0]

		data = {
		    'name': name,
		    'href': link,
		    'futbin_id': futbin_id
		}
		headers = {"Authorization": "Bearer " + str(token)}
		requests.post('http://127.0.0.1:8000/player/',
			data = data,
			headers = headers,
		)
		print(name, link, futbin_id)