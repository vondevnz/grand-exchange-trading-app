from pydantic import BaseModel, ConfigDict, Field, UUID4
from typing import Optional
from datetime import datetime

# Even though the Optional[str] works I should create default values eg. = None
class ItemsSchema(BaseModel):

	model_config = ConfigDict(from_attributes=True)

	item_id: int
	name: str
	item_image: Optional[str]
	instabuy: Optional[int]
	instasell: Optional[int]
	last_instabuy_time: Optional[datetime]
	last_instasell_time: Optional[datetime]

class ItemTimeStampsSchema(BaseModel):
	
	model_config = ConfigDict(from_attributes=True)

	id: UUID4
	timestamp: Optional[datetime]
	avg_high_price: Optional[int]
	avg_low_price: Optional[int]
	high_price_volume: Optional[int]
	low_price_volume: Optional[int]
	item_id: int