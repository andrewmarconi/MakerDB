export type Attachment = {
    id: string;
    filename: string;
    content_type: string;
    size: number;
    created_at: string;
};

export type Company = {
    id: string;
    name: string;
    website: string | null;
    is_manufacturer: boolean;
    is_vendor: boolean;
    created_at: string;
};

export type InventoryLocation = {
    id: string;
    name: string;
    description: string | null;
    children_count: number;
    created_at: string;
};

export type Order = {
    id: string;
    order_id: string;
    vendor: { name: string };
    status: string;
    total: number;
    date: string;
};

export type Part = {
    id: string;
    name: string;
    mpn: string;
    part_type: string;
    total_stock: number;
    manufacturer?: { name: string };
};

export type Project = {
    id: string;
    name: string;
    status: string;
    revision: string;
    updated_at: string;
};
