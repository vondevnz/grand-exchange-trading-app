from dotenv import load_dotenv
import os
import requests

def main():

    url = "https://prices.runescape.wiki/api/v1/osrs/latest?id=4151"

    load_dotenv()
    user_agent = os.getenv("USER_AGENT_TEXT")

    headers = {
        "User-Agent": user_agent
    }
    
    #response = requests.get(url, headers = headers)

    #print(response.text)


if __name__ == "__main__":
    main()
