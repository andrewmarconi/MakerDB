from typing import List
import csv
import io
from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from uuid import UUID
from projects.models import Project, BOMItem
from projects.schemas import (
    ProjectSchema,
    ProjectCreate,
    ProjectUpdate,
    BOMItemSchema,
    BOMItemCreate,
    BOMItemUpdate,
    BOMImportItem,
    BOMMatchResult,
)
from parts.models import Part
from asgiref.sync import sync_to_async

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/", response_model=List[ProjectSchema])
async def list_projects(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
):
    projects = await sync_to_async(list)(Project.objects.prefetch_related("attachments").all()[skip : skip + limit])
    return projects


@router.get("/count", response_model=dict)
async def count_projects():
    count = await sync_to_async(Project.objects.count)()
    return {"count": count}


@router.get("/{project_id}", response_model=ProjectSchema)
async def get_project(project_id: UUID):
    try:
        project = await sync_to_async(Project.objects.prefetch_related("attachments").get)(id=project_id)
        return project
    except Project.DoesNotExist:
        raise HTTPException(status_code=404, detail="Project not found")


@router.post("/", response_model=ProjectSchema, status_code=201)
async def create_project(data: ProjectCreate):
    try:
        project = await sync_to_async(lambda: Project.objects.create(**data.model_dump()))()
        project = await sync_to_async(lambda: Project.objects.prefetch_related("attachments").get(id=project.id))()
        return project
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{project_id}", response_model=ProjectSchema)
async def update_project(project_id: UUID, data: ProjectUpdate):
    try:
        project = await sync_to_async(Project.objects.get)(id=project_id)
    except Project.DoesNotExist:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    await sync_to_async(project.save)()
    project = await sync_to_async(Project.objects.prefetch_related("attachments").get)(id=project_id)
    return project


@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: UUID):
    try:
        project = await sync_to_async(Project.objects.get)(id=project_id)
        await sync_to_async(project.delete)()
    except Project.DoesNotExist:
        raise HTTPException(status_code=404, detail="Project not found")


@router.get("/{project_id}/bom", response_model=List[BOMItemSchema])
async def list_bom_items(project_id: UUID, skip: int = Query(0, ge=0), limit: int = Query(500, ge=1, le=1000)):
    bom_items = await sync_to_async(list)(
        BOMItem.objects.filter(project_id=project_id)
        .select_related("part", "part__manufacturer")
        .prefetch_related("substitutes")
        .all()[skip : skip + limit]
    )
    return bom_items


@router.post("/{project_id}/bom", response_model=BOMItemSchema, status_code=201)
async def add_bom_item(project_id: UUID, data: BOMItemCreate):
    try:
        project = await sync_to_async(Project.objects.get)(id=project_id)
    except Project.DoesNotExist:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        part = await sync_to_async(Part.objects.get)(id=data.part_id)
    except Part.DoesNotExist:
        raise HTTPException(status_code=404, detail="Part not found")

    @sync_to_async
    def _create():
        bom_item = BOMItem.objects.create(
            project=project, part=part, quantity=data.quantity, designators=data.designators or ""
        )
        if data.substitute_ids:
            substitutes = Part.objects.filter(id__in=data.substitute_ids)
            bom_item.substitutes.set(list(substitutes))
        return (
            BOMItem.objects.select_related("part", "part__manufacturer")
            .prefetch_related("substitutes")
            .get(id=bom_item.id)
        )

    try:
        bom_item = await _create()
        return bom_item
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{project_id}/bom/{item_id}", response_model=BOMItemSchema)
async def update_bom_item(project_id: UUID, item_id: UUID, data: BOMItemUpdate):
    try:
        bom_item = await sync_to_async(BOMItem.objects.select_related("part", "project").get)(
            id=item_id, project_id=project_id
        )
    except BOMItem.DoesNotExist:
        raise HTTPException(status_code=404, detail="BOM item not found")

    update_data = data.model_dump(exclude_unset=True)

    if "part_id" in update_data and update_data["part_id"]:
        try:
            new_part = await sync_to_async(Part.objects.get)(id=update_data["part_id"])
            bom_item.part = new_part
        except Part.DoesNotExist:
            raise HTTPException(status_code=404, detail="Part not found")
        del update_data["part_id"]

    for field, value in update_data.items():
        setattr(bom_item, field, value)

    await sync_to_async(bom_item.save)()
    bom_item = await sync_to_async(
        BOMItem.objects.select_related("part", "part__manufacturer").prefetch_related("substitutes").get
    )(id=item_id)
    return bom_item


@router.delete("/{project_id}/bom/{item_id}", status_code=204)
async def delete_bom_item(project_id: UUID, item_id: UUID):
    try:
        bom_item = await sync_to_async(BOMItem.objects.get)(id=item_id, project_id=project_id)
        await sync_to_async(bom_item.delete)()
    except BOMItem.DoesNotExist:
        raise HTTPException(status_code=404, detail="BOM item not found")


@router.post("/{project_id}/bom/import", response_model=List[BOMItemSchema])
async def import_bom_csv(project_id: UUID, file: UploadFile = File(...)):
    try:
        project = await sync_to_async(Project.objects.get)(id=project_id)
    except Project.DoesNotExist:
        raise HTTPException(status_code=404, detail="Project not found")

    content = await file.read()
    text_content = content.decode("utf-8")

    reader = csv.DictReader(io.StringIO(text_content))
    items = []

    for row in reader:
        quantity = int(row.get("quantity", row.get("Qty", 1)))
        part_number = row.get("part_number", row.get("Part Number", row.get("MPN", "")))
        reference = row.get("reference", row.get("Reference", row.get("Designator", "")))

        if part_number:
            try:
                part = await sync_to_async(Part.objects.get)(mpn=part_number)
            except Part.DoesNotExist:
                part = None
        else:
            part = None

        @sync_to_async
        def _create():
            bom_item = BOMItem.objects.create(
                project=project, part=part, quantity=quantity, designators=reference or ""
            )
            return (
                BOMItem.objects.select_related("part", "part__manufacturer")
                .prefetch_related("substitutes")
                .get(id=bom_item.id)
            )

        if part:
            bom_item = await _create()
            items.append(bom_item)

    return items


@router.post("/{project_id}/bom/match", response_model=List[BOMMatchResult])
async def match_bom_items(project_id: UUID, items: List[BOMImportItem]):
    results = []

    for item in items:
        result = BOMMatchResult(item=item, matched=False)

        if item.part_number:
            try:
                part = await sync_to_async(Part.objects.filter(mpn__icontains=item.part_number).first)()
                if part:
                    result.matched = True
                    result.part_id = part.id
                    result.part_name = part.name
                    result.confidence = "high"
            except Exception:
                pass

        results.append(result)

    return results


# --- Attachment Endpoints ---


@router.get("/{project_id}/attachments")
async def list_project_attachments(project_id: UUID):
    """List all attachments for a project."""
    try:
        project = await sync_to_async(Project.objects.prefetch_related("attachments").get)(id=project_id)
    except Project.DoesNotExist:
        raise HTTPException(status_code=404, detail="Project not found")

    attachments = await sync_to_async(lambda: list(project.attachments.all()))()
    return attachments


@router.post("/{project_id}/attachments")
async def upload_project_attachment(project_id: UUID, file: UploadFile = File(...)):
    """Upload a new attachment for a project."""
    try:
        project = await sync_to_async(Project.objects.get)(id=project_id)
    except Project.DoesNotExist:
        raise HTTPException(status_code=404, detail="Project not found")

    @sync_to_async
    def _create():
        content = file.file.read() if hasattr(file, "file") else b""
        file.file.seek(0)

        attachment = Attachment.objects.create(
            filename=file.filename or "unnamed",
            content_type=file.content_type or "application/octet-stream",
            size=file.size or 0,
            file=file.file,
        )
        project.attachments.add(attachment)
        return attachment

    try:
        attachment = await _create()
        return attachment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{project_id}/attachments/{attachment_id}", status_code=204)
async def delete_project_attachment(project_id: UUID, attachment_id: UUID):
    """Delete an attachment from a project."""
    try:
        project = await sync_to_async(Project.objects.get)(id=project_id)
    except Project.DoesNotExist:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        attachment = await sync_to_async(Attachment.objects.get)(id=attachment_id)
    except Attachment.DoesNotExist:
        raise HTTPException(status_code=404, detail="Attachment not found")

    await sync_to_async(project.attachments.remove)(attachment)
    await sync_to_async(attachment.delete)()
