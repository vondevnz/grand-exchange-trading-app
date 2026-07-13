from app.database import AsyncLocalSession
from app.models import Items
from sqlalchemy.dialects.postgresql import insert
import asyncio
from datetime import datetime 

dummy_items = [
    {
        "item_id": 4151,
        "name": "Abyssal whip",
        "item_image": "https://oldschool.runescape.wiki/images/Abyssal_whip.png",
        "instabuy": 2750000,
        "instasell": 2700000,
        "last_instabuy_time": datetime.fromisoformat("2026-07-11T14:32:00"),
        "last_instasell_time": datetime.fromisoformat("2026-07-11T14:30:00"),
    },
    {
        "item_id": 11840,
        "name": "Dragon claws",
        "item_image": "https://oldschool.runescape.wiki/images/Dragon_claws.png",
        "instabuy": 84500000,
        "instasell": 83200000,
        "last_instabuy_time": datetime.fromisoformat("2026-07-11T14:28:00"),
        "last_instasell_time": datetime.fromisoformat("2026-07-11T14:25:00"),
    },
]

# Open local session to poll data
async def pollData():
    async with AsyncLocalSession() as session:
        for item in dummy_items:
            stmt = insert(Items).values(
                    item_id=item.get("item_id"),
                    name=item.get("name"),
                    item_image=item.get("item_image"),
                    instabuy=item.get("instabuy"),
                    instasell=item.get("instasell"),
                    last_instabuy_time=item.get("last_instabuy_time"),
                    last_instasell_time=item.get("last_instasell_time")
                ).on_conflict_do_update(
                    index_elements=["item_id"], 
                    set_={
                        "instabuy": item.get("instabuy"),
                        "instasell": item.get("instasell"),
                        "last_instabuy_time": item.get("last_instabuy_time"),
                        "last_instasell_time": item.get("last_instasell_time")
                    }
                )
            await session.execute(stmt)
            await session.commit()

if __name__ == "__main__":
    asyncio.run(pollData())