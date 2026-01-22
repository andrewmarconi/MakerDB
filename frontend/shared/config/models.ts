export type ModelConfig = {
    apiPath: string;
    label: string;
    labelPlural: string;
    detailRoute: string;
    title: string;
    description: string;
    clickableColumn?: string;
};

export const MODEL_REGISTRY = {
    projects: {
        apiPath: '/db/projects',
        label: 'Project',
        labelPlural: 'Projects',
        detailRoute: '/projects',
        title: 'Projects',
        description: 'Manage your Bill of Materials and calculate production costs.',
        clickableColumn: 'name',
    },
    inventory: {
        apiPath: '/db/parts',
        label: 'Part',
        labelPlural: 'Parts',
        detailRoute: '/inventory',
        title: 'Inventory',
        description: 'Manage your parts and track stock levels.',
        clickableColumn: 'name',
    },
    locations: {
        apiPath: '/db/inventory/locations',
        label: 'Location',
        labelPlural: 'Locations',
        detailRoute: '/locations',
        title: 'Storage Locations',
        description: 'Browse and manage your storage locations.',
        clickableColumn: 'name',
    },
    companies: {
        apiPath: '/db/companies',
        label: 'Company',
        labelPlural: 'Companies',
        detailRoute: '/companies',
        title: 'Companies',
        description: 'Manage manufacturers and vendors.',
        clickableColumn: 'name',
    },
    purchasing: {
        apiPath: '/db/procurement/orders',
        label: 'Order',
        labelPlural: 'Orders',
        detailRoute: '/purchasing',
        title: 'Purchasing',
        description: 'Track your component orders and manage supplier relationships.',
        clickableColumn: 'order_id',
    },
} as const;

export type ModelKey = keyof typeof MODEL_REGISTRY;
