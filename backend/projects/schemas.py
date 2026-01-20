from typing import List, Optional, Annotated
from pydantic import BaseModel, Field, BeforeValidator
from uuid import UUID
from core.schemas import GlobalOpsSchema, AttachmentSchema, convert_m2m_to_list
from parts.schemas import PartSchema


class ProjectSchema(GlobalOpsSchema):
    name: str
    description: Optional[str] = ""
    notes: Optional[str] = ""
    status: str
    revision: str
    attachments: Annotated[List[AttachmentSchema], BeforeValidator(convert_m2m_to_list)] = Field(default_factory=list)


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    notes: Optional[str] = ""
    status: str = "draft"
    revision: str = "1.0"


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None
    revision: Optional[str] = None


class BOMItemSchema(GlobalOpsSchema):
    project_id: UUID
    part: PartSchema
    quantity: int
    designators: Optional[str] = ""
    substitutes: List[PartSchema] = Field(default_factory=list)


class BOMItemCreate(BaseModel):
    part_id: UUID
    quantity: int = 1
    designators: Optional[str] = ""
    substitute_ids: Optional[List[UUID]] = None


class BOMItemUpdate(BaseModel):
    part_id: Optional[UUID] = None
    quantity: Optional[int] = None
    designators: Optional[str] = None


class BOMImportItem(BaseModel):
    reference: Optional[str] = None
    quantity: int = 1
    part_number: Optional[str] = None
    description: Optional[str] = None


class BOMMatchResult(BaseModel):
    item: BOMImportItem
    matched: bool = False
    part_id: Optional[UUID] = None
    part_name: Optional[str] = None
    confidence: Optional[str] = None
