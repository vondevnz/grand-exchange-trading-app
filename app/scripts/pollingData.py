from app.database import AsyncLocalSession
from app.models import Items
from app.fetch import import_latest
from sqlalchemy.dialects.postgresql import insert
import asyncio
import json
from datetime import datetime, timezone

# Open local session to poll data
async def pollData():

    url="https://prices.runescape.wiki/api/v1/osrs/latest"

    response = import_latest(url)

    # Load the original JSON file
    with open("app/mappings/reversedItems.json", "r", encoding="utf-8") as file:
        ITEM_NAMES = json.load(file)

    # Load mapping JSON file (from Wiki)
    with open("app/mappings/mappingsData.json", "r", encoding="utf-8") as file:
        ITEM_MAPPINGS = json.load(file)

    icon_lookup = {item["id"]: item["icon"] for item in ITEM_MAPPINGS}

    async with AsyncLocalSession() as session:
        for item_id, price_data in list(response["data"].items()):

            item_name = ITEM_NAMES.get(item_id)
            item_icon = icon_lookup.get(int(item_id))
            item_url = f"https://oldschool.runescape.wiki/images/{item_icon.replace(' ', '_')}" if item_icon else None

            high = price_data.get("high")
            low = price_data.get("low")
            high_time = price_data.get("highTime")
            low_time = price_data.get("lowTime")

            if item_name is None or high is None or low is None or high_time is None or low_time is None:
                continue  # skip this item — incomplete price data

            stmt = insert(Items).values(
                    item_id=int(item_id),
                    name=item_name,
                    item_image=item_url,
                    instabuy=high,
                    instasell=low,
                    last_instabuy_time=datetime.fromtimestamp(high_time, tz=timezone.utc),
                    last_instasell_time=datetime.fromtimestamp(low_time, tz=timezone.utc)
                ).on_conflict_do_update(
                    index_elements=["item_id"], 
                    set_={
                        "item_image": item_url,
                        "instabuy": high,
                        "instasell": low,
                        "last_instabuy_time": datetime.fromtimestamp(high_time, tz=timezone.utc),
                        "last_instasell_time": datetime.fromtimestamp(low_time, tz=timezone.utc)
                    }
                )
            await session.execute(stmt)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(pollData())