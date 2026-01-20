from typing import List, Optional
from django.db.models import Sum, Q
from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from uuid import UUID
from parts.models import Part, Designator
from parts.schemas import (
    PartSchema,
    PartCreate,
    PartUpdate,
    TagsInput,
    DesignatorSchema,
    DesignatorCreate,
    DesignatorUpdate,
)
from core.models import Company, Attachment
from inventory.models import Storage
from projects.models import Project
from asgiref.sync import sync_to_async

router = APIRouter(prefix="/parts", tags=["Parts"])


def _get_part_queryset():
    from django.db.models import Sum, Q

    return (
        Part.objects.select_related("manufacturer", "default_storage")
        .prefetch_related("attachments")
        .annotate(total_stock=Sum("stock_entries__quantity", filter=Q(stock_entries__status__isnull=True)))
    )


@router.get("/", response_model=List[PartSchema])
async def list_parts(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
):
    """
    List parts with pagination support.
    """
    parts = await sync_to_async(list)(_get_part_queryset().all()[skip : skip + limit])
    return parts


@router.get("/count", response_model=dict)
async def count_parts():
    """
    Get total count of parts.
    """
    count = await sync_to_async(_get_part_queryset().count)()
    return {"count": count}


@router.get("/{part_id}", response_model=PartSchema)
async def get_part(part_id: UUID):
    try:
        part = await sync_to_async(_get_part_queryset().get)(id=part_id)
        return part
    except Part.DoesNotExist:
        raise HTTPException(status_code=404, detail="Part not found")


@router.post("/", response_model=PartSchema, status_code=201)
async def create_part(data: PartCreate):
    """Create a new part."""

    @sync_to_async
    def _create():
        part_data = data.model_dump(exclude={"manufacturer_id", "default_storage_id", "project_id"})
        part = Part(**part_data)

        if data.manufacturer_id:
            try:
                part.manufacturer = Company.objects.get(id=data.manufacturer_id, is_manufacturer=True)
            except Company.DoesNotExist:
                raise ValueError("Manufacturer not found")

        if data.default_storage_id:
            try:
                part.default_storage = Storage.objects.get(id=data.default_storage_id)
            except Storage.DoesNotExist:
                raise ValueError("Storage location not found")

        if data.project_id:
            try:
                part.project = Project.objects.get(id=data.project_id)
            except Project.DoesNotExist:
                raise ValueError("Project not found")

        part.save()
        return _get_part_queryset().get(id=part.id)

    try:
        part = await _create()
        return part
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{part_id}", response_model=PartSchema)
async def update_part(part_id: UUID, data: PartUpdate):
    """Update an existing part."""

    @sync_to_async
    def _update():
        try:
            part = Part.objects.get(id=part_id)
        except Part.DoesNotExist:
            raise ValueError("Part not found", 404)

        update_data = data.model_dump(exclude_unset=True)

        # Handle foreign key fields separately
        if "manufacturer_id" in update_data:
            mfr_id = update_data.pop("manufacturer_id")
            if mfr_id is None:
                part.manufacturer = None
            else:
                try:
                    part.manufacturer = Company.objects.get(id=mfr_id, is_manufacturer=True)
                except Company.DoesNotExist:
                    raise ValueError("Manufacturer not found", 400)

        if "default_storage_id" in update_data:
            storage_id = update_data.pop("default_storage_id")
            if storage_id is None:
                part.default_storage = None
            else:
                try:
                    part.default_storage = Storage.objects.get(id=storage_id)
                except Storage.DoesNotExist:
                    raise ValueError("Storage location not found", 400)

        if "project_id" in update_data:
            proj_id = update_data.pop("project_id")
            if proj_id is None:
                part.project = None
            else:
                try:
                    part.project = Project.objects.get(id=proj_id)
                except Project.DoesNotExist:
                    raise ValueError("Project not found", 400)

        # Update remaining fields
        for field, value in update_data.items():
            setattr(part, field, value)

        part.save()
        return _get_part_queryset().get(id=part.id)

    try:
        part = await _update()
        return part
    except ValueError as e:
        args = e.args
        detail = args[0] if args else "Error"
        status = args[1] if len(args) > 1 else 400
        raise HTTPException(status_code=status, detail=detail)


@router.delete("/{part_id}", status_code=204)
async def delete_part(part_id: UUID):
    """Delete a part."""

    @sync_to_async
    def _delete():
        try:
            part = Part.objects.get(id=part_id)
            part.delete()
            return True
        except Part.DoesNotExist:
            return False

    deleted = await _delete()
    if not deleted:
        raise HTTPException(status_code=404, detail="Part not found")


# --- Attachment endpoints ---


@router.post("/{part_id}/attachments", status_code=201)
async def upload_attachment(part_id: UUID, file: UploadFile = File(...)):
    """Upload an attachment to a part."""

    @sync_to_async
    def _upload():
        try:
            part = Part.objects.get(id=part_id)
        except Part.DoesNotExist:
            raise ValueError("Part not found", 404)

        # Determine file type from content type
        content_type = file.content_type or "application/octet-stream"
        file_type = "other"
        if content_type.startswith("image/"):
            file_type = "image"
        elif content_type == "application/pdf":
            file_type = "datasheet"

        attachment = Attachment.objects.create(
            filename=file.filename or "unnamed",
            content_type=content_type,
            file_type=file_type,
            size=file.size or 0,
            file=file.file,
        )
        part.attachments.add(attachment)
        return {"id": str(attachment.id), "filename": attachment.filename}

    try:
        result = await _upload()
        return result
    except ValueError as e:
        args = e.args
        raise HTTPException(status_code=args[1] if len(args) > 1 else 400, detail=args[0])


@router.delete("/{part_id}/attachments/{attachment_id}", status_code=204)
async def remove_attachment(part_id: UUID, attachment_id: UUID):
    """Remove an attachment from a part."""

    @sync_to_async
    def _remove():
        try:
            part = Part.objects.get(id=part_id)
        except Part.DoesNotExist:
            raise ValueError("Part not found", 404)

        try:
            attachment = part.attachments.get(id=attachment_id)
            part.attachments.remove(attachment)
            # Optionally delete the attachment entirely if not used elsewhere
            if not attachment.parts.exists():
                attachment.delete()
            return True
        except Attachment.DoesNotExist:
            raise ValueError("Attachment not found", 404)

    try:
        await _remove()
    except ValueError as e:
        args = e.args
        raise HTTPException(status_code=args[1] if len(args) > 1 else 400, detail=args[0])


# --- Tag endpoints ---


@router.post("/{part_id}/tags", response_model=List[str])
async def add_tags(part_id: UUID, data: TagsInput):
    """Add tags to a part."""

    @sync_to_async
    def _add_tags():
        try:
            part = Part.objects.get(id=part_id)
        except Part.DoesNotExist:
            raise ValueError("Part not found", 404)

        # Merge new tags with existing, avoiding duplicates
        existing_tags = set(part.tags or [])
        new_tags = set(data.tags)
        part.tags = list(existing_tags | new_tags)
        part.save(update_fields=["tags", "updated_at"])
        return part.tags

    try:
        tags = await _add_tags()
        return tags
    except ValueError as e:
        args = e.args
        raise HTTPException(status_code=args[1] if len(args) > 1 else 400, detail=args[0])


@router.delete("/{part_id}/tags/{tag}", response_model=List[str])
async def remove_tag(part_id: UUID, tag: str):
    """Remove a tag from a part."""

    @sync_to_async
    def _remove_tag():
        try:
            part = Part.objects.get(id=part_id)
        except Part.DoesNotExist:
            raise ValueError("Part not found", 404)

        tags = list(part.tags or [])
        if tag in tags:
            tags.remove(tag)
            part.tags = tags
            part.save(update_fields=["tags", "updated_at"])
        return part.tags

    try:
        tags = await _remove_tag()
        return tags
    except ValueError as e:
        args = e.args
        raise HTTPException(status_code=args[1] if len(args) > 1 else 400, detail=args[0])


# --- Designator endpoints ---

designator_router = APIRouter(prefix="/designators", tags=["Designators"])


@designator_router.get("/", response_model=List[DesignatorSchema])
async def list_designators():
    """List all designators."""
    designators = await sync_to_async(list)(Designator.objects.all())
    return designators


@designator_router.get("/{designator_id}", response_model=DesignatorSchema)
async def get_designator(designator_id: UUID):
    """Get a single designator by ID."""
    try:
        designator = await sync_to_async(Designator.objects.get)(id=designator_id)
        return designator
    except Designator.DoesNotExist:
        raise HTTPException(status_code=404, detail="Designator not found")


@designator_router.post("/", response_model=DesignatorSchema, status_code=201)
async def create_designator(data: DesignatorCreate):
    """Create a new designator."""

    @sync_to_async
    def _create():
        if Designator.objects.filter(code=data.code).exists():
            raise ValueError("Designator with this code already exists")
        designator = Designator.objects.create(code=data.code, name=data.name)
        return designator

    try:
        designator = await _create()
        return designator
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@designator_router.put("/{designator_id}", response_model=DesignatorSchema)
async def update_designator(designator_id: UUID, data: DesignatorUpdate):
    """Update a designator."""

    @sync_to_async
    def _update():
        try:
            designator = Designator.objects.get(id=designator_id)
        except Designator.DoesNotExist:
            raise ValueError("Designator not found", 404)

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(designator, field, value)

        designator.save()
        return designator

    try:
        designator = await _update()
        return designator
    except ValueError as e:
        args = e.args
        status = args[1] if len(args) > 1 else 400
        raise HTTPException(status_code=status, detail=args[0])


@designator_router.delete("/{designator_id}", status_code=204)
async def delete_designator(designator_id: UUID):
    """Delete a designator."""

    @sync_to_async
    def _delete():
        try:
            designator = Designator.objects.get(id=designator_id)
            designator.delete()
            return True
        except Designator.DoesNotExist:
            return False

    deleted = await _delete()
    if not deleted:
        raise HTTPException(status_code=404, detail="Designator not found")


# Include designator router in parts router
router.include_router(designator_router)
