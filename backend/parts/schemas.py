from typing import List, Optional, Dict, Any, Annotated
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from uuid import UUID
from core.schemas import GlobalOpsSchema, CompanySchema, AttachmentSchema, convert_m2m_to_list


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


class PartCreate(PartBase):
    """Schema for creating a new part."""

    manufacturer_id: Optional[UUID] = None
    default_storage_id: Optional[UUID] = None
    is_default_storage_mandatory: bool = False
    project_id: Optional[UUID] = None
    tags: List[str] = Field(default_factory=list)
    custom_fields: Dict[str, Any] = Field(default_factory=dict)


class PartUpdate(BaseModel):
    """Schema for updating a part. All fields optional."""

    part_type: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    footprint: Optional[str] = None
    mpn: Optional[str] = None
    cad_keys: Optional[List[str]] = None
    low_stock_threshold: Optional[int] = None
    attrition_percent: Optional[float] = None
    attrition_quantity: Optional[int] = None
    manufacturer_id: Optional[UUID] = None
    default_storage_id: Optional[UUID] = None
    is_default_storage_mandatory: Optional[bool] = None
    project_id: Optional[UUID] = None
    tags: Optional[List[str]] = None
    custom_fields: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(extra="forbid")


class TagsInput(BaseModel):
    """Schema for adding tags to a part."""

    tags: List[str]


class PartSchema(PartBase, GlobalOpsSchema):
    manufacturer: Optional[CompanySchema] = None
    default_storage_id: Optional[UUID] = Field(None, alias="default_storage_id")
    is_default_storage_mandatory: bool = False
    project_id: Optional[UUID] = Field(None, alias="project_id")
    attachments: Annotated[List[AttachmentSchema], BeforeValidator(convert_m2m_to_list)] = Field(default_factory=list)
    total_stock: int


class DesignatorSchema(GlobalOpsSchema):
    code: str
    name: str


class DesignatorCreate(BaseModel):
    code: str = Field(..., max_length=3)
    name: str = Field(..., max_length=128)


class DesignatorUpdate(BaseModel):
    code: Optional[str] = Field(None, max_length=3)
    name: Optional[str] = Field(None, max_length=128)
