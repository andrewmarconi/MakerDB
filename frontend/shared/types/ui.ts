export type ActionConfig = {
    label: string;
    icon: string;
    onClick: (row: any) => void;
    variant?: 'default' | 'destructive';
};

export type FilterConfig = {
    key: string;
    label: string;
    type: 'select' | 'input' | 'date';
    options?: { label: string; value: any }[];
};

export type CreateMode = 'single' | 'row' | 'grid';

export type RangeType = 'letters' | 'numbers';

/**
 * Common Props for DataTable component
 * @template T The type of data being displayed
 */
export type DataTableProps<T> = {
    /** Array of data items to display in the table */
    data: T[];
    /** Column definitions (TanStack Table ColumnDef format) */
    columns: any[];
    /** Display mode - 'table' for rows, 'grid' for cards (default: 'table') */
    viewMode?: 'table' | 'grid';
    /** Key for persisting view preferences in localStorage (default: route path) */
    storageKey?: string;
    /** Fields to display in grid/card view */
    cardFields: string[];
    /** Action buttons shown in card footer dropdown */
    cardActions?: ActionConfig[];
    /** Action buttons for table rows (not yet implemented) */
    tableActions?: ActionConfig[];
    /** Default sort configuration */
    defaultSort?: { id: string; desc: boolean };
    /** Enable search input in toolbar (default: false) */
    searchable?: boolean;
    /** Custom filter UI component (not yet implemented) */
    filterUI?: any;
    /** Show column visibility toggle dropdown (default: true) */
    showColumnToggle?: boolean;
    /** Enable pagination (default: true) */
    paginatable?: boolean;
    /** Number of items per page (default: 25) */
    itemsPerPage?: number;
    /** Column key that renders as a clickable link */
    clickableColumn?: string;
    /** Handler for row clicks - return { path } to navigate */
    onRowClick?: (row: T) => void | { path: string };
    /** Custom empty state content */
    emptyState?: string | any;
    /** Show loading skeleton */
    loading?: boolean;
    /** Route for creating new items (e.g., '/inventory/new') */
    createRoute?: string;
    /** Label for the create button (e.g., 'Add Part', 'New Order') */
    createLabel?: string;
};

// ============================================================================
// DataFormView Types
// ============================================================================

export type FieldType = 'text' | 'textarea' | 'number' | 'select' | 'checkbox' | 'tags' | 'search' | 'custom';

export type FieldSchema = {
    /** Field key in modelValue */
    key: string;
    /** Display label */
    label: string;
    /** Field type */
    type: FieldType;
    /** Whether field is required */
    required?: boolean;
    /** Placeholder text */
    placeholder?: string;
    /** Options for select type */
    options?: { label: string; value: any }[];
    /** API endpoint for search type */
    searchEndpoint?: string;
    /** Query parameter name for search (default: 'search') */
    searchQueryParam?: string;
    /** Search result label field (default: 'name') */
    searchLabelKey?: string;
    /** Search result value field (default: 'id') */
    searchValueKey?: string;
    /** Validation function - return error message or null */
    validator?: (value: any) => string | null;
    /** Field-level readonly */
    readonly?: boolean;
    /** Column span for two-column layout (1 or 2) */
    span?: 1 | 2;
    /** Custom component for 'custom' type */
    component?: any;
    /** Props to pass to custom component */
    componentProps?: Record<string, any>;
};

export type FieldState = 'idle' | 'editing' | 'saving' | 'success' | 'error';

export type DataFormViewProps = {
    /** v-model for the form data */
    modelValue: Record<string, any>;
    /** Field definitions */
    schema: FieldSchema[];
    /** API endpoint for PATCH/PUT */
    endpoint: string;
    /** ID for the entity */
    entityId: string;
    /** Save mode - 'patch' sends only changed field, 'put' sends full object */
    saveMode?: 'patch' | 'put';
    /** Debounce delay for auto-save in ms */
    debounceMs?: number;
    /** Layout mode */
    layout?: 'single' | 'two-column';
    /** Disable all editing */
    readonly?: boolean;
};

export type TabSchema = {
    key: string;
    label: string;
    icon?: string;
    fields: FieldSchema[];
};

export type DataFormViewTabsProps = {
    /** v-model for the form data */
    modelValue: Record<string, any>;
    /** Tab definitions with grouped fields */
    tabs: TabSchema[];
    /** API endpoint for PATCH/PUT */
    endpoint: string;
    /** ID for the entity */
    entityId: string;
    /** Save mode - 'patch' sends only changed field, 'put' sends full object */
    saveMode?: 'patch' | 'put';
    /** Debounce delay for auto-save in ms */
    debounceMs?: number;
    /** Layout mode */
    layout?: 'single' | 'two-column';
    /** Disable all editing */
    readonly?: boolean;
};

// ============================================================================
// DataFormInlineView Types
// ============================================================================

export type InlineDisplayColumn = {
    key: string;
    label: string;
    render?: (item: any) => any;
};

export type DataFormInlineViewProps = {
    /** List of related objects to display/edit */
    items: any[];
    /** Schema for editable fields (display + inline edit) */
    itemSchema: FieldSchema[];
    /** Non-editable display columns */
    displayColumns?: InlineDisplayColumn[];
    /** API endpoint base (e.g., '/projects/{id}/bom') */
    baseEndpoint: string;
    /** Section title */
    title: string;
    /** Add button label */
    addButtonLabel?: string;
    /** Empty state message */
    emptyStateMessage?: string;
    /** Allow editing */
    canEdit?: boolean;
    /** Allow deletion */
    canDelete?: boolean;
    /** Loading state */
    loading?: boolean;
};
