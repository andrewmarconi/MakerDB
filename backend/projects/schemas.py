from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID
from core.schemas import GlobalOpsSchema, AttachmentSchema
from parts.schemas import PartSchema

class ProjectSchema(GlobalOpsSchema):
    name: str
    description: Optional[str] = ""
    notes: Optional[str] = ""
    status: str
    revision: str
    attachments: List[AttachmentSchema] = Field(default_factory=list)

class BOMItemSchema(GlobalOpsSchema):
    project_id: UUID
    part: PartSchema
    quantity: int
    designators: Optional[str] = ""
    substitutes: List[PartSchema] = Field(default_factory=list)
