# Data Models

## Base Models

All models inherit from base classes in [backend/core/models.py](../../../backend/core/models.py):

### TimeStampedModel
```python
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

### GlobalOpsBase
```python
class GlobalOpsBase(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tags = models.JSONField(default=list, blank=True)
    custom_fields = models.JSONField(default=dict, blank=True)

    class Meta:
        abstract = True
```

All main entities (Part, Project, Order, etc.) inherit from `GlobalOpsBase`, providing:
- UUID primary keys
- Timestamps (created_at, updated_at)
- Tags (JSON array of strings)
- Custom fields (JSON object for flexible metadata)

## Django Apps and Models

| App | Models | Description |
|-----|--------|-------------|
| **core** | Company, Attachment | Base models and utilities |
| **parts** | Part, Designator | Component catalog |
| **inventory** | Storage, Lot, Stock | Storage locations and inventory tracking |
| **projects** | Project, BOMItem | Projects and bills of materials |
| **procurement** | Order, Offer | Purchase orders and vendor pricing |

## Model Relationships

```
Company (Manufacturer/Vendor)
    ↓ (1:N)
Part ← (M:N) → Attachment
    ↓ (1:N)
Stock → Storage (Location)
    ↑ (N:1)
Lot

Project
    ↓ (1:N)
BOMItem → Part
```
