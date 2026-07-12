from dotenv import load_dotenv
import os
import json
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from database import get_db

from schemas import ItemsSchema, ItemTimeStampsSchema

load_dotenv()
USER_AGENT = os.getenv("USER_AGENT_TEXT")

app = FastAPI(
    title="Grand Exchange Trading Application",
    version="1.0.0",
    description="Real-time pricing and filtering for GE items"
)

# Allow your React dev server to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default dev port
    allow_methods=["*"],
    allow_headers=["*"],
)

dummy_items = [
    {
        "item_id": 4151,
        "name": "Abyssal whip",
        "item_image": "https://oldschool.runescape.wiki/images/Abyssal_whip.png",
        "instabuy": 2750000,
        "instasell": 2700000,
        "last_instabuy_time": "2026-07-11T14:32:00",
        "last_instasell_time": "2026-07-11T14:30:00",
    },
    {
        "item_id": 11840,
        "name": "Dragon claws",
        "item_image": "https://oldschool.runescape.wiki/images/Dragon_claws.png",
        "instabuy": 84500000,
        "instasell": 83200000,
        "last_instabuy_time": "2026-07-11T14:28:00",
        "last_instasell_time": "2026-07-11T14:25:00",
    },
]

# Load the original JSON file
# with open("mappings/reversedItems.json", "r", encoding="utf-8") as file:
    # ITEM_NAMES = json.load(file)


@app.get("/api/prices/latest", response_model=list[ItemsSchema])
async def get_latest_prices(db: AsyncSession = Depends(get_db)):
    stmt = select(Items)
    result = await db.execute(stmt)
    return result.scalars().all()

@app.get("/api/prices/latest/{item_id}", response_model=ItemsSchema)
def get_item(item_id: int):
    for item in dummy_items:
        if item.get("item_id") == item_id:
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")



