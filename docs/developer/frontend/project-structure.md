# Project Structure

```
frontend/
├── app/                      # Source directory (srcDir in nuxt.config.ts)
│   ├── components/          # Vue components
│   │   ├── Dashboard/       # Dashboard-specific components
│   │   ├── Files/           # File/attachment components
│   │   ├── Search/          # Search-related components
│   │   ├── Tags/            # Tag management components
│   │   └── *.vue            # Global components
│   ├── layouts/             # Layout components
│   │   └── default.vue      # Main application layout
│   ├── pages/               # File-based routing
│   │   ├── index.vue        # Dashboard (/)
│   │   ├── inventory/       # Inventory pages
│   │   ├── locations/       # Storage locations
│   │   ├── projects/        # Projects and BOMs
│   │   ├── purchasing/      # Purchase orders
│   │   ├── companies/       # Companies (manufacturers/vendors)
│   │   └── designators/     # PCB designators
│   ├── assets/              # Static assets
│   │   └── css/            # Global CSS
│   ├── composables/         # Vue composables (auto-imported)
│   ├── utils/               # Utility functions (auto-imported)
│   └── app.vue             # Root application component
├── public/                  # Static files (served at root)
│   └── favicon.png
├── nuxt.config.ts          # Nuxt configuration
├── tailwind.config.ts      # Tailwind configuration
├── tsconfig.json           # TypeScript configuration
├── vitest.config.ts        # Vitest configuration
└── package.json            # Dependencies and scripts
```

## Auto-imports
Nuxt automatically imports:
- Components from `app/components/`
- Composables from `app/composables/`
- Utils from `app/utils/`
- Vue APIs (ref, computed, watch, etc.)
- Nuxt APIs (useState, useFetch, navigateTo, etc.)
