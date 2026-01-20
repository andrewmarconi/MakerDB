# MakerDB Implementation Tasks

## Status Overview
- ✅ **Phase 1-9**: Core UI, navigation, data display, and backend integration complete
- 🚧 **Current Focus**: Full CRUD operations and interactive workflows
- 📋 **Remaining**: Advanced features, optimization, and production readiness

---

## Backend: API CRUD Operations

### Parts Management
- [x] POST `/api/parts/` - Create new part
- [x] PUT `/api/parts/{id}` - Update part details
- [x] DELETE `/api/parts/{id}` - Delete part
- [x] POST `/api/parts/{id}/attachments` - Upload attachments
- [x] DELETE `/api/parts/{id}/attachments/{attachment_id}` - Remove attachment
- [x] POST `/api/parts/{id}/tags` - Add tags
- [x] DELETE `/api/parts/{id}/tags/{tag}` - Remove tag

### Inventory & Storage
- [x] POST `/api/inventory/locations` - Create storage location
- [x] PUT `/api/inventory/locations/{id}` - Update location
- [x] DELETE `/api/inventory/locations/{id}` - Delete location
- [x] POST `/api/inventory/stock` - Add stock entry
- [x] PUT `/api/inventory/stock/{id}` - Adjust stock quantity
- [x] DELETE `/api/inventory/stock/{id}` - Remove stock entry
- [x] POST `/api/inventory/lots` - Create lot/batch
- [x] PUT `/api/inventory/lots/{id}` - Update lot details

### Projects & BOM
- [x] POST `/api/projects/` - Create project
- [x] PUT `/api/projects/{id}` - Update project
- [x] DELETE `/api/projects/{id}` - Delete project
- [x] POST `/api/projects/{id}/bom` - Add BOM item
- [x] PUT `/api/projects/{id}/bom/{item_id}` - Update BOM item
- [x] DELETE `/api/projects/{id}/bom/{item_id}` - Remove BOM item
- [x] POST `/api/projects/{id}/bom/import` - Import BOM from CSV
- [x] POST `/api/projects/{id}/bom/match` - Auto-match BOM items to parts

### Procurement
- [ ] POST `/api/procurement/orders` - Create purchase order
- [ ] PUT `/api/procurement/orders/{id}` - Update order
- [ ] DELETE `/api/procurement/orders/{id}` - Cancel order
- [ ] POST `/api/procurement/orders/{id}/receive` - Receive order items
- [ ] POST `/api/procurement/offers` - Create vendor offer
- [ ] PUT `/api/procurement/offers/{id}` - Update offer
- [ ] DELETE `/api/procurement/offers/{id}` - Remove offer

---

## Frontend: Interactive Forms & Pages

> **Design Principles**: 
> - Use dedicated pages/routes for complex forms. Reserve modals only for simple confirmations, quick actions, and lightweight interactions.
> - For complex data entry with many fields, use tabs to organize information into logical sections (e.g., Basic Info, Specifications, Stock, Attachments).
> - This makes forms more digestible and reduces cognitive load.

### Parts & Inventory
- [x] Create `/inventory/new` page for adding parts
  - [x] **Tab 1: Basic Info**
    - [x] Part type selection (Linked, Local, Meta, Sub-assembly)
    - [x] Name/title
    - [x] MPN (for Linked parts)
    - [x] Manufacturer (for Linked parts)
    - [x] Description
    - [x] Category/tags
  - [x] **Tab 2: Specifications**
    - [x] Custom fields (key-value pairs)
    - [x] Parametric data (resistance, capacitance, etc.)
    - [x] Package/footprint
    - [x] Datasheet URL
  - [x] **Tab 3: Initial Stock** (optional)
    - [x] Quantity
    - [x] Location
    - [x] Lot information
    - [x] Purchase price
  - [x] **Tab 4: Attachments** (optional)
    - [x] File upload area
    - [x] Image gallery
- [x] Create `/inventory/{id}/edit` page for editing parts
  - [x] Same tabbed structure as creation
  - [x] Pre-populate with existing data
- [x] Implement StockAdjustmentModal functionality (simple modal is OK)
  - [x] Connect to POST `/api/inventory/stock`
  - [x] Support Add/Set/Remove operations
  - [x] Multi-location stock updates
  - [x] Lot/batch assignment
- [x] Implement AttachmentManager functionality (inline component)
  - [x] File upload with drag-and-drop
  - [x] Preview for images/PDFs
  - [x] Delete attachments
- [x] Implement TagManager functionality (inline component)
  - [x] Add new tags
  - [x] Remove tags
  - [x] Tag autocomplete

### Storage Locations
- [x] Create `/locations/new` page for adding locations
  - [x] **Mode Selection**: Single, Row, or Grid
  - [x] **Single Mode**:
    - [x] Name, description, parent location
    - [ ] Location type selector
  - [x] **Row Mode**:
    - [x] Prefix input (e.g., "Box1-")
    - [x] Range type selector (Letters or Numbers)
    - [x] Range input (e.g., "A-Z" or "1-20")
    - [x] Dynamic preview of generated names
    - [x] Count indicator (e.g., "Creating 26 locations")
    - [x] Parent location selector
  - [x] **Grid Mode**:
    - [x] Prefix input (e.g., "Shelf-")
    - [x] Row range type (Letters or Numbers)
    - [x] Row range input (e.g., "A-D")
    - [x] Column range type (Letters or Numbers)
    - [x] Column range input (e.g., "1-8")
    - [x] Dynamic preview grid visualization
    - [x] Count indicator (e.g., "Creating 32 locations")
    - [x] Parent location selector
  - [x] **Preview Component**:
    - [x] Real-time update as user types
    - [x] Show first N items + "... and X more"
    - [x] Highlight naming conflicts if any exist
- [x] Create `/locations/{id}/edit` page for editing locations
- [x] Add delete confirmation modal (simple modal is OK)
- [ ] Add location move/reorganize functionality

### Companies (Manufacturers & Vendors)

**Backend API (Completed)**
- [x] GET `/api/core/companies` - List companies with filtering
- [x] GET `/api/core/companies/{id}` - Get company by ID
- [x] POST `/api/core/companies` - Create new company
- [x] PUT `/api/core/companies/{id}` - Update company
- [x] DELETE `/api/core/companies/{id}` - Delete company

**Frontend UI**
- [x] Create `/companies` page for listing companies
  - [x] Filter by type (Manufacturer / Vendor)
  - [x] Search by name
  - [x] Add/Edit/Delete actions per row
- [x] Create `/companies/new` page for adding companies
  - [x] Company name
  - [x] Website URL
  - [x] Type toggle (Manufacturer / Vendor / Both)
  - [x] Contact information (email, phone, address)
- [x] Create `/companies/{id}/edit` page for editing companies
  - [x] Same fields as creation
  - [ ] Show parts manufactured by this company
  - [ ] Show orders from this vendor
- [x] Add "Companies" link to sidebar (under Inventory section)

### Projects & BOM
- [x] Create `/projects/new` page for creating projects
  - [x] Project name, description, status
  - [ ] Initial BOM setup
- [x] Create `/projects/{id}/edit` page for editing projects
- [x] Create `/projects/{id}/bom/import` page for BOM import
  - [x] CSV/TSV file upload
  - [x] Column mapping interface
  - [x] Preview imported data
  - [x] Auto-match to existing parts
- [x] Enhance `/projects/{id}` BOM tab with inline editing
  - [x] Update quantity, designators inline
  - [ ] Assign matched part via dropdown/search
  - [ ] Set substitutes
- [ ] Implement BOM matching workflow
  - [ ] Manual part selection
  - [ ] Substitute assignment
  - [ ] Unmatched items highlighting

### Purchasing
- [ ] Create `/purchasing/new` page for creating orders
  - [ ] Vendor selection
  - [ ] Add line items
  - [ ] Calculate totals
- [ ] Create `/purchasing/{id}/edit` page for editing orders
- [ ] Create `/purchasing/{id}/receive` page for receiving orders
  - [ ] Quantity verification
  - [ ] Location assignment
  - [ ] Lot creation
  - [ ] Update stock levels
- [ ] Implement order status transitions (Open → Ordered → Received)

---

## Advanced Features

### Search & Discovery
- [ ] Implement global search (Cmd+K)
  - [ ] Search across parts, projects, orders
  - [ ] Quick navigation
  - [ ] Recent items
- [ ] Implement ParametricSearch component
  - [ ] Unit-aware filtering (10k = 10000)
  - [ ] Range queries
  - [ ] Multiple parameter filters
- [ ] Add advanced filters to list views
  - [ ] Date ranges
  - [ ] Stock level filters
  - [ ] Status filters

### Labels & Printing
- [ ] Implement LabelPreview functionality
  - [ ] QR code generation for parts/locations
  - [ ] Label template selection
  - [ ] Print configuration
  - [ ] Batch printing
- [ ] Add barcode scanning support
  - [ ] Camera-based scanning
  - [ ] HID scanner support
  - [ ] Quick lookup by scan

### Reporting & Analytics
- [ ] Enhance dashboard components with real calculations
  - [ ] Actual inventory valuation from stock data
  - [ ] Real storage occupancy metrics
  - [ ] Dynamic low stock alerts
- [ ] Add export functionality
  - [ ] Export BOMs to CSV
  - [ ] Export inventory reports
  - [ ] Export order history
- [ ] Create additional reports
  - [ ] Stock movement history
  - [ ] Project cost analysis
  - [ ] Vendor performance

---

## Data Validation & Error Handling

### Backend
- [ ] Add comprehensive input validation
  - [ ] Required field checks
  - [ ] Format validation (MPNs, emails, etc.)
  - [ ] Unique constraint enforcement
- [ ] Implement proper error responses
  - [ ] Standardized error format
  - [ ] Helpful error messages
  - [ ] Validation error details
- [ ] Add transaction support for complex operations
  - [ ] Order receiving (stock + lot creation)
  - [ ] BOM import (multiple items)

### Frontend
- [ ] Add form validation
  - [ ] Required field indicators
  - [ ] Format validation (numbers, dates)
  - [ ] Real-time validation feedback
- [ ] Implement error handling
  - [ ] Toast notifications for errors
  - [ ] Retry mechanisms for failed requests
  - [ ] Offline detection
- [ ] Add loading states
  - [ ] Skeleton loaders for tables
  - [ ] Button loading indicators
  - [ ] Page-level loading states

---

## Testing & Quality

### Backend Tests
- [ ] Unit tests for routers
  - [ ] Test all CRUD endpoints
  - [ ] Test validation logic
  - [ ] Test error cases
- [ ] Integration tests
  - [ ] Test complete workflows (create order → receive)
  - [ ] Test data relationships
  - [ ] Test transaction rollbacks

### Frontend Tests
- [ ] Component tests
  - [ ] Test form submissions
  - [ ] Test modal interactions
  - [ ] Test table sorting/filtering
- [ ] E2E tests
  - [ ] Test critical user flows
  - [ ] Test navigation
  - [ ] Test data persistence

---

## Performance & Optimization

- [ ] Backend optimization
  - [ ] Add database indexes
  - [ ] Optimize N+1 queries
  - [ ] Add pagination to list endpoints
  - [ ] Implement caching where appropriate
- [ ] Frontend optimization
  - [ ] Lazy load components
  - [ ] Virtualize long lists
  - [ ] Optimize bundle size
  - [ ] Add service worker for offline support

---

## Production Readiness

### Security
- [ ] Implement authentication
  - [ ] User login/logout
  - [ ] Session management
  - [ ] Password reset
- [ ] Add authorization
  - [ ] Role-based access control
  - [ ] Permission checks on endpoints
  - [ ] UI permission hiding
- [ ] Security hardening
  - [ ] CSRF protection
  - [ ] Rate limiting
  - [ ] Input sanitization

### Deployment
- [ ] Environment configuration
  - [ ] Production settings
  - [ ] Environment variables
  - [ ] Secrets management
- [ ] Database migrations
  - [ ] Migration scripts
  - [ ] Rollback procedures
  - [ ] Seed data
- [ ] Monitoring & logging
  - [ ] Error tracking (Sentry)
  - [ ] Performance monitoring
  - [ ] Access logs

### Documentation
- [ ] API documentation
  - [ ] OpenAPI/Swagger docs
  - [ ] Endpoint descriptions
  - [ ] Example requests/responses
- [ ] User documentation
  - [ ] Getting started guide
  - [ ] Feature walkthroughs
  - [ ] FAQ
- [ ] Developer documentation
  - [ ] Setup instructions
  - [ ] Architecture overview
  - [ ] Contributing guidelines

---

## Nice-to-Have Features

- [ ] Real-time updates (WebSockets)
  - [ ] Live stock level updates
  - [ ] Collaborative BOM editing
  - [ ] Order status notifications
- [ ] Advanced BOM features
  - [ ] BOM versioning
  - [ ] BOM comparison
  - [ ] Cost optimization suggestions
- [ ] Inventory forecasting
  - [ ] Usage trend analysis
  - [ ] Reorder point suggestions
  - [ ] Lead time tracking
- [ ] Mobile app
  - [ ] Native iOS/Android apps
  - [ ] Barcode scanning
  - [ ] Quick stock checks
