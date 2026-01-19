from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from core.schemas import GlobalOpsSchema, AttachmentSchema


# --- Storage Schemas ---

class StorageCreate(BaseModel):
    """Schema for creating a storage location."""
    name: str
    description: Optional[str] = ""
    tags: List[str] = Field(default_factory=list)
    custom_fields: Dict[str, Any] = Field(default_factory=dict)


class StorageUpdate(BaseModel):
    """Schema for updating a storage location."""
    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    custom_fields: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(extra="forbid")


class StorageSchema(GlobalOpsSchema):
    name: str
    description: Optional[str] = ""
    attachments: List[AttachmentSchema] = Field(default_factory=list)


# --- Lot Schemas ---

class LotCreate(BaseModel):
    """Schema for creating a lot/batch."""
    name: str
    description: Optional[str] = ""
    comments: Optional[str] = ""
    expiration_date: Optional[datetime] = None
    order_id: Optional[UUID] = None
    tags: List[str] = Field(default_factory=list)
    custom_fields: Dict[str, Any] = Field(default_factory=dict)


class LotUpdate(BaseModel):
    """Schema for updating a lot/batch."""
    name: Optional[str] = None
    description: Optional[str] = None
    comments: Optional[str] = None
    expiration_date: Optional[datetime] = None
    order_id: Optional[UUID] = None
    tags: Optional[List[str]] = None
    custom_fields: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(extra="forbid")


class LotSchema(GlobalOpsSchema):
    name: str
    description: Optional[str] = ""
    comments: Optional[str] = ""
    expiration_date: Optional[datetime] = None
    attachments: List[AttachmentSchema] = Field(default_factory=list)
    order_id: Optional[UUID] = None


# --- Stock Schemas ---

class StockCreate(BaseModel):
    """Schema for creating a stock entry."""
    part_id: UUID
    storage_id: UUID
    lot_id: Optional[UUID] = None
    quantity: int = 0
    status: Optional[str] = None
    price_unit: Optional[Decimal] = None
    currency: Optional[str] = ""
    tags: List[str] = Field(default_factory=list)
    custom_fields: Dict[str, Any] = Field(default_factory=dict)


class StockUpdate(BaseModel):
    """Schema for updating a stock entry."""
    storage_id: Optional[UUID] = None
    lot_id: Optional[UUID] = None
    quantity: Optional[int] = None
    status: Optional[str] = None
    price_unit: Optional[Decimal] = None
    currency: Optional[str] = None
    tags: Optional[List[str]] = None
    custom_fields: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(extra="forbid")


class StockSchema(GlobalOpsSchema):
    part_id: UUID
    storage: StorageSchema
    lot: Optional[LotSchema] = None
    quantity: int
    status: Optional[str] = None
    price_unit: Optional[float] = None
    currency: Optional[str] = ""
