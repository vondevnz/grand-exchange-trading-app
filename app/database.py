import ssl
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Connection URL
DATABASE_URL = os.getenv("DATABASE_URL")

connect_args = {}
if "neon.tech" in DATABASE_URL:
	connect_args["ssl"] = ssl.create_default_context()

engine = create_async_engine(
	DATABASE_URL,
	echo = True,
	connect_args=connect_args,
)

# Create session factory
AsyncLocalSession = sessionmaker(
	bind = engine,
	class_ = AsyncSession,
	expire_on_commit = False
)

# Base class for models (tables will inherit from this)
Base = declarative_base()

# Dependacy for FastAPI routes -> gets DB session
async def get_db():
	async with AsyncLocalSession() as session:
		try:
			yield session
			await session.commit()
		except Exception:
			await session.rollback()
			raise
		finally:
			await session.close()