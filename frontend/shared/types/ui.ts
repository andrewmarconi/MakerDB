export type tActionConfig = {
    label: string;
    icon: string;
    onClick: (row: any) => void;
    variant?: 'default' | 'destructive';
};

export type tFilterConfig = {
    key: string;
    label: string;
    type: 'select' | 'input' | 'date';
    options?: { label: string; value: any }[];
};

export type tCreateMode = 'single' | 'row' | 'grid';

export type tRangeType = 'letters' | 'numbers';

// ============================================================================
// DataTable Types (deprecated, kept for reference during migration)
// ============================================================================

export type tDataTableProps<T> = {
    data: T[];
    columns: any[];
    viewMode?: 'table' | 'grid';
    storageKey?: string;
    cardFields: string[];
    cardActions?: tActionConfig[];
    tableActions?: tActionConfig[];
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
    createRoute?: string;
    createLabel?: string;
};

// ============================================================================
// DataListView Types
// ============================================================================

export type tDataListViewProps = {
    modelKey: string;
    columnDefs: any[];
    cardFields?: string[];
    viewMode?: 'table' | 'grid';
    canView?: boolean;
    canDelete?: boolean;
    canCreate?: boolean;
    canSearch?: boolean;
    canColumnToggle?: boolean;
    canPaginate?: boolean;
    defaultSort?: { id: string; desc: boolean };
    itemsPerPage?: number;
    createLabel?: string;
    emptyMessage?: string;
    detailRoute?: string;
    cardActions?: tActionConfig[];
    tableActions?: tActionConfig[];
    filters?: tFilterConfig[];
};

// ============================================================================
// DataFormView Types
// ============================================================================

export type tFieldType = 'text' | 'textarea' | 'number' | 'select' | 'checkbox' | 'tags' | 'search' | 'custom';

export type tFieldSchema = {
    key: string;
    label: string;
    type: tFieldType;
    required?: boolean;
    placeholder?: string;
    options?: { label: string; value: any }[];
    searchEndpoint?: string;
    searchQueryParam?: string;
    searchLabelKey?: string;
    searchValueKey?: string;
    validator?: (value: any) => string | null;
    readonly?: boolean;
    span?: 1 | 2;
    component?: any;
    componentProps?: Record<string, any>;
};

export type tFieldState = 'idle' | 'editing' | 'saving' | 'success' | 'error';

export type tDataFormViewProps = {
    modelValue: Record<string, any>;
    schema: tFieldSchema[];
    endpoint: string;
    entityId: string;
    saveMode?: 'patch' | 'put';
    debounceMs?: number;
    layout?: 'single' | 'two-column';
    readonly?: boolean;
};

export type tTabSchema = {
    key: string;
    label: string;
    icon?: string;
    fields: tFieldSchema[];
};

export type tDataFormViewTabsProps = {
    modelValue: Record<string, any>;
    tabs: tTabSchema[];
    endpoint: string;
    entityId: string;
    saveMode?: 'patch' | 'put';
    debounceMs?: number;
    layout?: 'single' | 'two-column';
    readonly?: boolean;
};

// ============================================================================
// DataFormInlineView Types
// ============================================================================

export type tInlineDisplayColumn = {
    key: string;
    label: string;
    render?: (item: any) => any;
};

export type tDataFormInlineViewProps = {
    items: any[];
    itemSchema: tFieldSchema[];
    displayColumns?: tInlineDisplayColumn[];
    baseEndpoint: string;
    title: string;
    addButtonLabel?: string;
    emptyStateMessage?: string;
    canEdit?: boolean;
    canDelete?: boolean;
    loading?: boolean;
};

// ============================================================================
// Model Registry Types
// ============================================================================

export type tModelConfig = {
    apiPath: string;
    label: string;
    labelPlural: string;
    detailRoute: string;
    title: string;
    description: string;
    clickableColumn?: string;
};
