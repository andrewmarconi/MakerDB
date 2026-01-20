# API Development

## Creating a New Endpoint

### 1. Define Pydantic Schema (`schemas.py`)

```python
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class PartBase(BaseModel):
    name: str
    description: str | None = None
    manufacturer_id: UUID | None = None

class PartCreate(PartBase):
    pass

class PartUpdate(PartBase):
    name: str | None = None  # Make fields optional for PATCH

class PartSchema(PartBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
```

### 2. Create Endpoint (`router.py`)

```python
from fastapi import APIRouter, HTTPException
from asgiref.sync import sync_to_async
from .models import Part
from .schemas import PartSchema, PartCreate, PartUpdate

router = APIRouter(prefix="/parts", tags=["Parts"])

@router.get("/", response_model=list[PartSchema])
async def list_parts():
    parts = await sync_to_async(list)(Part.objects.all())
    return parts

@router.post("/", response_model=PartSchema, status_code=201)
async def create_part(data: PartCreate):
    @sync_to_async
    def _create():
        part = Part(**data.model_dump())
        part.save()
        return part

    return await _create()

@router.put("/{part_id}", response_model=PartSchema)
async def update_part(part_id: UUID, data: PartUpdate):
    @sync_to_async
    def _update():
        try:
            part = Part.objects.get(id=part_id)
        except Part.DoesNotExist:
            raise ValueError("Part not found")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(part, field, value)
        part.save()
        return part

    try:
        return await _update()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{part_id}", status_code=204)
async def delete_part(part_id: UUID):
    @sync_to_async
    def _delete():
        try:
            part = Part.objects.get(id=part_id)
            part.delete()
        except Part.DoesNotExist:
            raise ValueError("Part not found")

    try:
        await _delete()
    except ValueError:
        raise HTTPException(status_code=404, detail="Part not found")
```

### 3. Register Router (in `makerdb/api.py`)

```python
from parts.router import router as parts_router

app.include_router(parts_router)
```

## Query Optimization

Use `select_related()` and `prefetch_related()` to avoid N+1 queries:

```python
def _get_part_queryset():
    return (
        Part.objects
        .select_related("manufacturer", "default_storage")
        .prefetch_related("attachments")
        .annotate(total_stock=Sum("stock_entries__quantity"))
    )

@router.get("/")
async def list_parts():
    parts = await sync_to_async(list)(_get_part_queryset())
    return parts
```

## Pagination

```python
from fastapi import Query

@router.get("/")
async def list_parts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    parts = await sync_to_async(list)(
        Part.objects.all()[skip:skip + limit]
    )
    return parts
```
