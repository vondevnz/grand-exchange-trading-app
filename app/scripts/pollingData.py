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

    async with AsyncLocalSession() as session:
        for item_id, price_data in list(response["data"].items())[:30]:

            item_name = ITEM_NAMES.get(item_id)
            item_url = str(item_name).replace(' ', '_')

            stmt = insert(Items).values(
                    item_id=int(item_id),
                    name=item_name,
                    item_image=f"https://oldschool.runescape.wiki/images/{item_url}.png",
                    instabuy=price_data.get("high"),
                    instasell=price_data.get("low"),
                    last_instabuy_time=datetime.fromtimestamp(price_data.get("highTime"), tz=timezone.utc),
                    last_instasell_time=datetime.fromtimestamp(price_data.get("lowTime"), tz=timezone.utc)
                ).on_conflict_do_update(
                    index_elements=["item_id"], 
                    set_={
                        "item_image": f"https://oldschool.runescape.wiki/images/{item_url}.png",
                        "instabuy": price_data.get("high"),
                        "instasell": price_data.get("low"),
                        "last_instabuy_time": datetime.fromtimestamp(price_data.get("highTime"), tz=timezone.utc),
                        "last_instasell_time": datetime.fromtimestamp(price_data.get("lowTime"), tz=timezone.utc)
                    }
                )
            await session.execute(stmt)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(pollData())