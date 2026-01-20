# Bulk Storage Location Creation - Implementation Spec

## Overview
Allow users to create multiple storage locations at once using prefix + range patterns.

## Modes

### 1. Single Location
Standard form for creating one location at a time.

### 2. Row of Locations
Creates a linear sequence of locations.

**Input:**
- Prefix: `Box1-`
- Range Type: `Letters` or `Numbers`
- Range: `A-Z` or `1-20`

**Output Examples:**
- `Box1-A`, `Box1-B`, `Box1-C`, ..., `Box1-Z` (26 locations)
- `Box1-1`, `Box1-2`, `Box1-3`, ..., `Box1-20` (20 locations)

### 3. Grid of Locations
Creates a 2D grid of locations (rows × columns).

**Input:**
- Prefix: `Shelf-`
- Row Range Type: `Letters` or `Numbers`
- Row Range: `A-D`
- Column Range Type: `Letters` or `Numbers`
- Column Range: `1-8`

**Output Examples:**
- `Shelf-A1`, `Shelf-A2`, ..., `Shelf-A8`
- `Shelf-B1`, `Shelf-B2`, ..., `Shelf-B8`
- `Shelf-C1`, `Shelf-C2`, ..., `Shelf-C8`
- `Shelf-D1`, `Shelf-D2`, ..., `Shelf-D8`
- Total: 32 locations (4 rows × 8 columns)

## Range Parsing Logic

### Letter Ranges
- Format: `A-Z`, `a-z`, `AA-AZ`, etc.
- Case-insensitive input, preserve case in output
- Support multi-character ranges (e.g., `AA-ZZ`)
- Validation: Start must be <= End alphabetically

### Number Ranges
- Format: `1-100`, `001-999` (with zero-padding)
- Preserve zero-padding from input
- Validation: Start must be <= End numerically
- Max range: 1000 locations (prevent accidental huge ranges)

## Preview Component

### Display Rules
- Show first 10 items
- If more than 10: show "... and X more locations"
- Display in a grid for Grid mode, list for Row mode
- Update in real-time as user types

### Validation Warnings
- ⚠️ Duplicate names detected
- ⚠️ Names conflict with existing locations
- ⚠️ Range too large (>1000 locations)
- ⚠️ Invalid range format

## UI Flow

```
┌─────────────────────────────────────┐
│  Create Storage Locations           │
├─────────────────────────────────────┤
│                                     │
│  Mode: ○ Single  ● Row  ○ Grid     │
│                                     │
│  Prefix: [Box1-____________]        │
│                                     │
│  Range Type: ● Letters  ○ Numbers  │
│                                     │
│  Range: [A___] to [Z___]           │
│                                     │
│  Parent Location: [Select...]      │
│                                     │
├─────────────────────────────────────┤
│  Preview (26 locations)             │
│  ┌───────────────────────────────┐ │
│  │ Box1-A  Box1-B  Box1-C       │ │
│  │ Box1-D  Box1-E  Box1-F       │ │
│  │ Box1-G  Box1-H  Box1-I       │ │
│  │ ... and 17 more locations    │ │
│  └───────────────────────────────┘ │
├─────────────────────────────────────┤
│              [Cancel] [Create All] │
└─────────────────────────────────────┘
```

## Backend API

### Endpoint
`POST /api/inventory/locations/bulk`

### Request Body
```json
{
  "mode": "row",
  "prefix": "Box1-",
  "range_type": "letters",
  "range_start": "A",
  "range_end": "Z",
  "parent_id": "uuid-of-parent",
  "description": "Optional description template"
}
```

Or for grid:
```json
{
  "mode": "grid",
  "prefix": "Shelf-",
  "row_range_type": "letters",
  "row_range_start": "A",
  "row_range_end": "D",
  "col_range_type": "numbers",
  "col_range_start": "1",
  "col_range_end": "8",
  "parent_id": "uuid-of-parent"
}
```

### Response
```json
{
  "created": 26,
  "locations": [
    {"id": "uuid1", "name": "Box1-A"},
    {"id": "uuid2", "name": "Box1-B"},
    ...
  ]
}
```

## Frontend Utilities

### `generateLocationNames(config)`
```typescript
interface LocationConfig {
  mode: 'single' | 'row' | 'grid'
  prefix: string
  rangeType?: 'letters' | 'numbers'
  rangeStart?: string
  rangeEnd?: string
  rowRangeType?: 'letters' | 'numbers'
  rowRangeStart?: string
  rowRangeEnd?: string
  colRangeType?: 'letters' | 'numbers'
  colRangeStart?: string
  colRangeEnd?: string
}

// Returns: string[] of generated location names
```

### `parseRange(start: string, end: string, type: 'letters' | 'numbers')`
```typescript
// Returns: string[] of values in range
// Examples:
// parseRange('A', 'C', 'letters') => ['A', 'B', 'C']
// parseRange('1', '3', 'numbers') => ['1', '2', '3']
// parseRange('001', '003', 'numbers') => ['001', '002', '003']
```

## Edge Cases

1. **Empty prefix**: Allow, but warn if it creates generic names like "1", "2", "3"
2. **Reverse ranges**: Auto-swap if user enters Z-A instead of A-Z
3. **Single item range**: Allow (e.g., A-A creates just "A")
4. **Very large ranges**: Warn and require confirmation if >100 locations
5. **Existing names**: Check for conflicts before creation, show warning
6. **Special characters in prefix**: Allow, but sanitize for filesystem safety

## Future Enhancements

- 3D Grid mode (Row × Column × Depth)
- Custom separators (e.g., "Box1_A" instead of "Box1-A")
- Template variables (e.g., "{prefix}{row}{col}" → "Shelf-A1")
- Batch QR code generation for all created locations
- CSV import for arbitrary location names
