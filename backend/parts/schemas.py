from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID
from core.schemas import GlobalOpsSchema, CompanySchema, AttachmentSchema

class PartBase(BaseModel):
    part_type: str
    name: str
    description: Optional[str] = ""
    notes: Optional[str] = ""
    footprint: Optional[str] = ""
    mpn: Optional[str] = ""
    cad_keys: List[str] = Field(default_factory=list)
    low_stock_threshold: Optional[int] = None
    attrition_percent: float = 0.0
    attrition_quantity: int = 0

class PartSchema(PartBase, GlobalOpsSchema):
    manufacturer: Optional[CompanySchema] = None
    # We'll use a forward reference or ID for default_storage to avoid circular deps
    default_storage_id: Optional[UUID] = Field(None, alias="default_storage_id")
    is_default_storage_mandatory: bool = False
    project_id: Optional[UUID] = Field(None, alias="project_id")
    attachments: List[AttachmentSchema] = Field(default_factory=list)
    total_stock: int
