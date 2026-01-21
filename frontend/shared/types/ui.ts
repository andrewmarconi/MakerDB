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
