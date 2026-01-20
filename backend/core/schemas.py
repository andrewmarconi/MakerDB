from datetime import datetime
from uuid import UUID
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


def convert_m2m_to_list(value):
    """Convert Django ManyRelatedManager to list for Pydantic serialization."""
    if hasattr(value, "all"):
        return list(value.all())
    return value


class TimeStampedSchema(BaseModel):
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class GlobalOpsSchema(TimeStampedSchema):
    id: UUID
    tags: List[str] = Field(default_factory=list)
    custom_fields: Dict[str, Any] = Field(default_factory=dict)


class CompanySchema(GlobalOpsSchema):
    name: str
    website: Optional[str] = None
    is_manufacturer: bool = False
    is_vendor: bool = False
    contacts: List[Dict[str, Any]] = Field(default_factory=list)


class CompanyCreate(BaseModel):
    """Schema for creating a company."""

    name: str
    website: Optional[str] = None
    is_manufacturer: bool = False
    is_vendor: bool = False
    contacts: List[Dict[str, Any]] = Field(default_factory=list)


class AttachmentSchema(TimeStampedSchema):
    id: UUID
    file_type: str
    filename: str
    content_type: str
    size: int
    file_url: Optional[str] = Field(None, alias="file")

    # We might want to compute the full URL if we use Media storage
    @property
    def url(self) -> Optional[str]:
        return self.file_url
