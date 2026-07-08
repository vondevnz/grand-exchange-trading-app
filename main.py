from dotenv import load_dotenv
import os
import requests
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
USER_AGENT = os.getenv("USER_AGENT_TEXT")

app = FastAPI()

# Allow your React dev server to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default dev port
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/prices/latest")
def get_latest_prices():
    headers = {
        "User-Agent": USER_AGENT
    }

    # Load the original JSON file
    with open("mappings/items.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    item_id = data["Yew sapling"]

    url = f"https://prices.runescape.wiki/api/v1/osrs/latest?id={item_id}"

    response = requests.get(url, headers = headers)

    response.raise_for_status()

    print(response.text)

    return response.json()
