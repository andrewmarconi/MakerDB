from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from uuid import UUID
from core.schemas import GlobalOpsSchema, CompanySchema, AttachmentSchema
from parts.schemas import PartSchema

class OrderSchema(GlobalOpsSchema):
    vendor: CompanySchema
    number: str
    invoice_number: Optional[str] = ""
    po_number: Optional[str] = ""
    comments: Optional[str] = ""
    notes: Optional[str] = ""
    expected_arrival: Optional[datetime] = None
    status: str
    attachments: List[AttachmentSchema] = Field(default_factory=list)

class OfferSchema(GlobalOpsSchema):
    offer_type: str
    vendor: Optional[CompanySchema] = None
    sku: Optional[str] = ""
    moq: int = 1
    order_multiple: int = 1
    prices: List[Dict[str, Any]] = Field(default_factory=list)
    in_stock_status: Optional[str] = None
    reference: Optional[str] = ""
    comments: Optional[str] = ""
    url: Optional[str] = ""
    expires_at: Optional[datetime] = None
    part: Optional[PartSchema] = None
    attachments: List[AttachmentSchema] = Field(default_factory=list)
