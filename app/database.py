from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Connection URL
DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/items_db"

engine = create_async_engine(
	DATABASE_URL,
	echo = True
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