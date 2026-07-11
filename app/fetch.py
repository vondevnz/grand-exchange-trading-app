from dotenv import load_dotenv
import os
import requests
import json

def import_latest(url):
	load_dotenv()
	USER_AGENT = os.getenv("USER_AGENT_TEXT")

	headers = {
		"User-Agent": USER_AGENT
	}
	response = requests.get(url, headers=headers)
	response.raise_for_status()
	return response.json()