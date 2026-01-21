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
    data: T[];
    columns: any[]; // Using any here to avoid tanstack dependency in declaration file if not needed
    viewMode?: 'table' | 'grid';
    storageKey?: string;
    cardFields: string[];
    cardActions?: ActionConfig[];
    tableActions?: ActionConfig[];
    defaultSort?: { id: string; desc: boolean };
    searchable?: boolean;
    filterUI?: any;
    showColumnToggle?: boolean;
    paginatable?: boolean;
    itemsPerPage?: number;
    clickableColumn?: string;
    onRowClick?: (row: T) => void | { path: string };
    emptyState?: string | any;
    loading?: boolean;
};

// ============================================================================
// DataFormView Types
// ============================================================================

export type FieldType = 'text' | 'textarea' | 'number' | 'select' | 'checkbox' | 'tags' | 'custom';

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
