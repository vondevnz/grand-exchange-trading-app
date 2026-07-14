from dotenv import load_dotenv
import os
import json
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from app.database import get_db, Base, engine
from app.models import Items

from app.schemas import ItemsSchema, ItemTimeStampsSchema

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


@app.get("/api/prices/latest", response_model=list[ItemsSchema])
async def get_latest_prices(search: str | None = None, db: AsyncSession = Depends(get_db)):
    stmt = select(Items)
    if search:
        stmt = stmt.where(Items.name.ilike(f"%{search}%"))
    result = await db.execute(stmt)
    return result.scalars().all()

@app.get("/api/prices/latest/{item_id}", response_model=ItemsSchema)
def get_item(item_id: int):
    for item in dummy_items:
        if item.get("item_id") == item_id:
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
