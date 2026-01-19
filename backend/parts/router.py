from typing import List
from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from parts.models import Part
from parts.schemas import PartSchema
from asgiref.sync import sync_to_async

router = APIRouter(prefix="/parts", tags=["Parts"])

@router.get("/", response_model=List[PartSchema])
async def list_parts():
    # Django 0RM async compatibility
    parts = await sync_to_async(list)(Part.objects.select_related('manufacturer', 'default_storage').prefetch_related('attachments').all())
    return parts

@router.get("/{part_id}", response_model=PartSchema)
async def get_part(part_id: UUID):
    try:
        part = await sync_to_async(Part.objects.select_related('manufacturer', 'default_storage').prefetch_related('attachments', 'specs').get)(id=part_id)
        return part
    except Part.DoesNotExist:
        raise HTTPException(status_code=404, detail="Part not found")
