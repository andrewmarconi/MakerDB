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

class BOMItemSchema(GlobalOpsSchema):
    project_id: UUID
    part: PartSchema
    quantity: int
    designators: Optional[str] = ""
    substitutes: List[PartSchema] = Field(default_factory=list)
