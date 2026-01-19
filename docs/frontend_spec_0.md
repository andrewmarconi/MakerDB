# MakerDB Frontend Specification

## 1. Workflows

### 1.1 Inventory Management
MakerDB offers a robust inventory management system tracking electronic components, storage locations, and stock levels.

- **Part Types**:
    - **Linked Parts**: Components with distinct Manufacturer Part Numbers (MPNs) and online data (datasheets, specs).
    - **Local Parts**: Generic components, PCBs, custom parts without MPNs.
    - **Meta-parts**: Groupings of interchangeable parts (exact substitutes).
    - **Sub-assembly parts**: Result of building projects (1:1 correspondence with projects).
- **Stock Control**:
    - Tracks physical quantity on hand.
    - Multi-location support (e.g., full reels vs. cut tape).
    - **Lot Control**: Tracks specific batches (source, date, price) for traceability (FIFO/LIFO usage).
- **Storage Locations**:
    - Hierarchical naming (e.g., `b01-a4` for box 1, row a, col 4).
    - Supports single locations, rows, grids, and 3D grids.
    - Default storage locations can be assigned to parts (optional or mandatory).

### 1.2 Projects (BOM)
A Project represents a Bill of Materials (BOM) for a design or product.

- **BOM Management**:
    - Import BOMs from CAD via CSV/TSV.
    - **Matching**: Automatch BOM entries to existing parts by MPN or name.
    - **Substitutes**:
        - **Part Substitutes**: Global equivalents (e.g., generic resistors).
        - **BOM Substitutes**: Project-specific alternatives for a specific BOM line.
- **Pricing**:
    - Fetches online prices from distributors (checking MOQs, price breaks, currency).
    - Integrates local stock value.
    - Allows manual "Local Offers" for custom supplier pricing.
    - Optimization: Automatically selects best offers based on build quantity and "Price Discarding Excess".

### 1.3 Purchasing
Manage procurement of components.

- **Order States**:
    - **Open**: Modifiable, building the list.
    - **Ordered**: Finalized and placed with vendor (locked).
    - **Received**: Parts arrived and added to inventory.

### 1.4 [Descoped]
Builds and Production workflows are currently out of scope.

## 2. Core Features

### 2.1 Search & Filtering
- **Search**: Fuzzy search across Name, MPN, Manufacturer, Description, Footprint, and Custom Fields.
- **Filtering**: Advanced specific filters per table (e.g., "[Storage] Tags"). Supports logical AND/OR and nested conditions.
- **Presets**: Save filter configurations and column layouts as Personal or Company-wide presets.
- **Parametric Search**: Filter by numerical values with unit prefixes (e.g., `10k`, `22u`).

### 2.2 Barcode Scanning & Labeling
- **ID Anything™**: Unique codes for parts, lots, builds, and storage locations.
- **Labeling**: Print QR codes/labels for lots and devices for quick scanning and access to data.
- **Device Tracking**: Scan a device label to view its entire build history and test results.

### 2.3 Custom Data
- **Custom Fields**: Structured additional data for parts, lots, orders, etc. (e.g., "Distributor Part Number", "Bin Location"). Indexed for search.
- **Attachments**: Link files (datasheets, invoices, images) to parts, lots, and orders.
- **Tags**: Flexible categorization (e.g., `#smd`, `#connector`) for search and bulk operations.

### 2.4 Reporting
- **Real-time Reports**: "Low Stock", "Inventory Valuation".
- **Valuation**: Tracks "Purchase Value" (money spent) and "Replacement Value". Lot control enables exact cost tracking per batch.

## 3. Integrations

### 3.1 CAD Integration
- **BOM Import**: Supports CSV/TSV export from major ECAD tools (Altium, KiCad, etc.).
- **Column Mapping**: Heuristic matching of CSV columns to MakerDB fields (Quantity, MPN, Designators).
- **Altium Fixes**: Handles known CSV escaping bugs from Altium Designer.

### 3.2 API & Data Exchange
- **CSV Export**: Export lists of parts, orders, or build histories to CSV.
- **API**: (Implied) Backend mounted at `/api/` (FastAPI) for programmatic access to inventory and operations.
