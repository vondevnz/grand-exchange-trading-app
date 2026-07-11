from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

# creates sql items table for Items (inherits Base)
class Items(Base):
	__tablename__ = "items"

	item_id = Column(Integer, primary_key = True)
	name = Column(String(100), nullable = False)
	item_image = Column(String(200))
	instabuy = Column(Integer)
	instasell = Column(Integer)
	last_instabuy_time = Column(DateTime)
	last_instasell_time = Column(DateTime)

# creates sql items table for Items (inherits Base)
class ItemTimeStamps(Base):
	__tablename__ = "item_time_stamp"

	id = Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
	timestamp = Column(DateTime)
	avg_high_price = Column(Integer)
	avg_low_price = Column(Integer)
	high_price_volume = Column(Integer)
	low_price_volume = Column(Integer)
	item_id = Column(Integer, ForeignKey("items.item_id"), nullable = False)

