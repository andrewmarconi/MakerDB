# Coding Conventions

## Python Style

- **Line length**: 120 characters (configured in `pyproject.toml`)
- **Type hints**: Use modern syntax (`list[str]` not `List[str]`)
- **Imports**: Organized by ruff (stdlib, third-party, local)
- **Docstrings**: Use for public APIs and complex logic

## Django Models

```python
from django.db import models
from core.models import GlobalOpsBase

class Part(GlobalOpsBase):
    """
    Represents a physical component in the inventory.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    manufacturer = models.ForeignKey(
        "core.Company",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="parts"
    )

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return self.name
```

## Pydantic Schemas

```python
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime

class PartSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None = None
    manufacturer_id: UUID | None = None
    created_at: datetime
    updated_at: datetime

    # Computed fields
    total_stock: int = Field(default=0, description="Total quantity in stock")
```

## Error Handling

```python
from fastapi import HTTPException

@router.get("/{part_id}")
async def get_part(part_id: UUID):
    @sync_to_async
    def _get():
        try:
            return Part.objects.get(id=part_id)
        except Part.DoesNotExist:
            raise ValueError("Part not found")

    try:
        return await _get()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
```

## Async Patterns

```python
# DO: Wrap Django ORM in sync_to_async
@sync_to_async
def _get_parts():
    return list(Part.objects.all())

parts = await _get_parts()

# DON'T: Direct ORM calls in async context
# This will fail!
parts = await Part.objects.all()  # ❌
```
