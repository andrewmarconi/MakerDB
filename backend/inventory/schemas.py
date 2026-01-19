from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID
from core.schemas import GlobalOpsSchema, AttachmentSchema

class StorageSchema(GlobalOpsSchema):
    name: str
    description: Optional[str] = ""
    attachments: List[AttachmentSchema] = Field(default_factory=list)

class LotSchema(GlobalOpsSchema):
    name: str
    description: Optional[str] = ""
    comments: Optional[str] = ""
    expiration_date: Optional[datetime] = None
    attachments: List[AttachmentSchema] = Field(default_factory=list)
    order_id: Optional[UUID] = None

class StockSchema(GlobalOpsSchema):
    part_id: UUID
    storage: StorageSchema
    lot: Optional[LotSchema] = None
    quantity: int
    status: Optional[str] = None
    price_unit: Optional[float] = None
    currency: Optional[str] = ""
