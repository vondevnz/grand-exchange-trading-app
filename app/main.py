from dotenv import load_dotenv
import os
import json
import math
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from app.database import get_db, Base, engine
from app.models import Items
from app.scripts.pollingData import pollData

from app.schemas import ItemsSchema, ItemTimeStampsSchema, PaginatedItemsResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler

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

@app.on_event("startup")
async def create_tables():
    # Create all database tables defined in models if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Database tables successfully created")

    await pollData()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(pollData, 'interval', minutes=10)
    scheduler.start()

@app.get("/api/prices/latest", response_model=PaginatedItemsResponse)
async def get_latest_prices(page: int = 1, page_size: int = 20, search: str | None = None, db: AsyncSession = Depends(get_db)):

    stmt = select(Items).limit(page_size).offset((page- 1) * page_size)
    if search:
        stmt = stmt.where(Items.name.ilike(f"%{search}%"))

    # Number of items
    count_stmt = select(func.count()).select_from(Items)
    if search:
        count_stmt = count_stmt.where(Items.name.ilike(f"%{search}%"))

    result = await db.execute(stmt)
    count = await db.execute(count_stmt)
    count_result = count.scalar()
    return {
        "items": result.scalars().all(),
        "total": count_result,
        "page": page,
        "page_size": page_size,
        "total_pages": math.ceil(count_result / page_size)
    }

@app.get("/api/prices/latest/{item_id}", response_model=ItemsSchema)
def get_item(item_id: int):
    for item in dummy_items:
        if item.get("item_id") == item_id:
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
