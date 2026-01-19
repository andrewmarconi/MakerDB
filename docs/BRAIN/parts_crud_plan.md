# Backend Parts Management - Implementation Plan

## Overview
Implement full CRUD operations for parts management, including creating, updating, and deleting parts along with their associated data (attachments, tags, custom fields).

## Endpoints to Implement

### 1. Create Part
**Endpoint**: `POST /api/parts/`

**Request Body**:
```json
{
  "name": "STM32F103C8T6",
  "mpn": "STM32F103C8T6",
  "manufacturer_id": "uuid-of-stmicro",
  "part_type": "linked",
  "description": "ARM Cortex-M3 MCU, 64KB Flash, 20KB RAM",
  "category": "Microcontrollers",
  "datasheet_url": "https://...",
  "package": "LQFP48",
  "custom_fields": {
    "core": "ARM Cortex-M3",
    "frequency": "72MHz",
    "flash": "64KB"
  },
  "tags": ["mcu", "arm", "stm32"],
  "default_location_id": "uuid-of-location"
}
```

**Response**: `201 Created`
```json
{
  "id": "uuid",
  "name": "STM32F103C8T6",
  "mpn": "STM32F103C8T6",
  "part_type": "linked",
  "created_at": "2026-01-19T14:00:00Z",
  ...
}
```

**Validation**:
- `name` is required
- `part_type` must be one of: `linked`, `local`, `meta`, `sub_assembly`
- `mpn` required for `linked` parts
- `manufacturer_id` should exist if provided
- `custom_fields` must be valid JSON object
- `tags` must be array of strings

### 2. Update Part
**Endpoint**: `PUT /api/parts/{id}`

**Request Body**: Same as create, all fields optional
**Response**: `200 OK` with updated part

**Validation**:
- Part must exist
- Cannot change `part_type` after creation
- Same validation rules as create

### 3. Delete Part
**Endpoint**: `DELETE /api/parts/{id}`

**Response**: `204 No Content`

**Validation**:
- Part must exist
- Check for dependencies:
  - ⚠️ Warn if part has stock (soft delete or require force flag)
  - ⚠️ Warn if part is in active BOMs
  - ⚠️ Warn if part has open orders

### 4. Manage Attachments
**Endpoint**: `POST /api/parts/{id}/attachments`

**Request**: Multipart form data
```
file: <binary>
description: "Datasheet"
type: "datasheet"
```

**Response**: `201 Created`
```json
{
  "id": "uuid",
  "filename": "stm32f103.pdf",
  "url": "/media/attachments/...",
  "type": "datasheet",
  "size": 1024000,
  "uploaded_at": "2026-01-19T14:00:00Z"
}
```

**Delete Attachment**: `DELETE /api/parts/{id}/attachments/{attachment_id}`

### 5. Manage Tags
**Endpoint**: `POST /api/parts/{id}/tags`

**Request Body**:
```json
{
  "tags": ["new-tag", "another-tag"]
}
```

**Response**: `200 OK` with updated part

**Delete Tag**: `DELETE /api/parts/{id}/tags/{tag}`

## Implementation Steps

### Step 1: Update Parts Router
- [ ] Add POST endpoint for creating parts
- [ ] Add PUT endpoint for updating parts
- [ ] Add DELETE endpoint for deleting parts
- [ ] Add attachment management endpoints
- [ ] Add tag management endpoints

### Step 2: Create Request/Response Schemas
- [ ] `PartCreateSchema` - for POST requests
- [ ] `PartUpdateSchema` - for PUT requests (all fields optional)
- [ ] `AttachmentUploadSchema` - for file uploads
- [ ] `TagsSchema` - for tag management

### Step 3: Implement Business Logic
- [ ] Part creation with validation
- [ ] Part update with partial updates
- [ ] Part deletion with dependency checks
- [ ] File upload handling
- [ ] Tag management (add/remove)

### Step 4: Add Validation
- [ ] Required field validation
- [ ] Part type validation
- [ ] Foreign key validation (manufacturer, location)
- [ ] Custom fields JSON validation
- [ ] File type/size validation for attachments

### Step 5: Error Handling
- [ ] 400 Bad Request for validation errors
- [ ] 404 Not Found for missing parts
- [ ] 409 Conflict for constraint violations
- [ ] 422 Unprocessable Entity for business rule violations

## Database Considerations

### Transactions
Use database transactions for operations that modify multiple tables:
- Creating part with initial stock
- Deleting part with cascading deletes
- Updating part with tag changes

### File Storage
- Store uploaded files in `MEDIA_ROOT/attachments/`
- Generate unique filenames to avoid collisions
- Store file metadata in `Attachment` model
- Clean up orphaned files on attachment deletion

### Custom Fields
- Store as JSON in `custom_fields` field
- No strict schema validation (flexible)
- Consider indexing for common fields if needed

## Testing Plan

### Unit Tests
- [ ] Test part creation with valid data
- [ ] Test part creation with invalid data
- [ ] Test part update (full and partial)
- [ ] Test part deletion
- [ ] Test attachment upload
- [ ] Test tag management

### Integration Tests
- [ ] Test creating part with manufacturer
- [ ] Test creating part with initial stock
- [ ] Test deleting part with stock (should warn/fail)
- [ ] Test file upload and retrieval
- [ ] Test tag filtering

## Next Steps After Parts Management

1. **Inventory Management** - Stock CRUD operations
2. **Storage Locations** - Location CRUD with bulk creation
3. **Projects & BOM** - Project and BOM item management
4. **Procurement** - Order creation and receiving workflow
