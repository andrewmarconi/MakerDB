from typing import List
from fastapi import APIRouter, HTTPException
from uuid import UUID
from projects.models import Project, BOMItem
from projects.schemas import ProjectSchema, BOMItemSchema
from asgiref.sync import sync_to_async

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=List[ProjectSchema])
async def list_projects():
    projects = await sync_to_async(list)(Project.objects.prefetch_related('attachments').all())
    return projects

@router.get("/{project_id}", response_model=ProjectSchema)
async def get_project(project_id: UUID):
    try:
        project = await sync_to_async(Project.objects.prefetch_related('attachments').get)(id=project_id)
        return project
    except Project.DoesNotExist:
        raise HTTPException(status_code=404, detail="Project not found")

@router.get("/{project_id}/bom", response_model=List[BOMItemSchema])
async def list_bom_items(project_id: UUID):
    bom_items = await sync_to_async(list)(BOMItem.objects.filter(project_id=project_id).select_related('part', 'part__manufacturer').prefetch_related('substitutes').all())
    return bom_items
