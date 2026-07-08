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
    with open("mappings/reversedItems.json", "r", encoding="utf-8") as file:
        ITEM_NAMES = json.load(file)

    url = f"https://prices.runescape.wiki/api/v1/osrs/latest"

    response = requests.get(url, headers = headers)

    response.raise_for_status()

    prices = response.json()["data"]

    combined = []
    for item_id, price_data in prices.items():
        combined.append({
            "id": item_id,
            "name": ITEM_NAMES.get(item_id, "Unknown"),
            "high": price_data.get("high"),
            "low": price_data.get("low"),
            "highTime": price_data.get("highTime"),
            "lowTime": price_data.get("lowTime"),
        })

    return combined