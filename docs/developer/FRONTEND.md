# Frontend Development Guide

This guide covers everything you need to know to develop and contribute to the MakerDB frontend application.

## Table of Contents

- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Package Overview](#package-overview)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Coding Conventions](#coding-conventions)
- [Component Development](#component-development)
- [API Integration](#api-integration)
- [Common Tasks](#common-tasks)

## Overview

The MakerDB frontend is built with **Nuxt 4**, a modern Vue 3 framework with server-side rendering capabilities. It provides a responsive, accessible interface for inventory management with a focus on usability and performance.

### Key Features
- Server-side rendering (SSR) for improved SEO and initial load performance
- Component-based architecture with Nuxt UI v4
- Type-safe development with TypeScript
- Comprehensive testing with Vitest
- Modern styling with Tailwind CSS 4

## Technology Stack

### Core Framework
- **Nuxt 4** (`^4.2.2`) - Vue 3 meta-framework with SSR
- **Vue 3** (`^3.5.26`) - Progressive JavaScript framework
- **Vue Router** (`^4.6.4`) - Official router for Vue.js
- **TypeScript** (`^5.9.3`) - Type-safe JavaScript

### UI & Styling
- **Nuxt UI v4** (`^4.3.0`) - Component library built on Tailwind CSS
- **Tailwind CSS 4** (`^4.1.18`) - Utility-first CSS framework
- **@tailwindcss/vite** (`^4.1.18`) - Vite plugin for Tailwind
- **@iconify-json/heroicons** (`^1.2.3`) - Icon library

### Development Tools
- **Nuxt ESLint** (`^1.12.1`) - Code quality and consistency
- **Vitest** (`^3.2.4`) - Fast unit test framework
- **@nuxt/test-utils** (`^3.23.0`) - Testing utilities for Nuxt
- **@vue/test-utils** (`^2.4.6`) - Official testing utilities for Vue
- **Concurrently** (`^9.1.2`) - Run multiple commands simultaneously

### Additional Modules
- **@nuxt/image** (`^2.0.0`) - Optimized image component
- **@nuxt/a11y** (`^1.0.0-alpha.1`) - Accessibility tools and auditing
- **@nuxt/hints** (`^1.0.0-alpha.5`) - Development hints and suggestions

## Package Overview

### Nuxt UI v4
Nuxt UI provides pre-built, accessible components that follow best practices. Key components include:
- **Forms**: Input, Select, Textarea, Checkbox, Radio, Toggle
- **Data Display**: Table, Badge, Card, Avatar
- **Navigation**: Button, Dropdown, Modal, Tabs
- **Feedback**: Alert, Toast, Progress, Skeleton
- **Layout**: Container, Divider, AspectRatio

**Documentation**: https://ui.nuxt.com/

### Tailwind CSS 4
The latest version of Tailwind provides:
- Oxide engine for improved performance
- Native CSS cascade layers
- Modern container queries
- Built-in color palette with semantic naming

**Documentation**: https://tailwindcss.com/

### Vitest
Modern testing framework with:
- Native ESM support
- Lightning-fast test execution
- Vue component testing
- Two test projects: `unit` (Node environment) and `nuxt` (happy-dom for component testing)

**Documentation**: https://vitest.dev/

## Project Structure

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

### Auto-imports
Nuxt automatically imports:
- Components from `app/components/`
- Composables from `app/composables/`
- Utils from `app/utils/`
- Vue APIs (ref, computed, watch, etc.)
- Nuxt APIs (useState, useFetch, navigateTo, etc.)

## Getting Started

### Prerequisites
- Node.js 18+ (check with `node --version`)
- npm or yarn
- Backend server running on http://localhost:8000

### Initial Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**
   ```bash
   npm run dev
   ```

   The application will be available at http://localhost:3000

3. **Run with backend** (recommended)
   ```bash
   npm run dev:all
   ```

   This starts both the backend and frontend servers concurrently.

### Configuration

#### Environment Variables
Nuxt environment variables are configured in `nuxt.config.ts`. Currently, the app uses Nitro route rules for API proxying:

```typescript
nitro: {
  routeRules: {
    '/db/**': { proxy: 'http://localhost:8000/api/**' }
  }
}
```

This proxies frontend requests from `/db/**` to the backend API at `/api/**`.

## Development Workflow

### File-based Routing
Nuxt uses file-based routing. Pages are automatically generated based on the file structure in `app/pages/`:

- `pages/index.vue` → `/`
- `pages/inventory/index.vue` → `/inventory`
- `pages/inventory/[id]/index.vue` → `/inventory/:id` (dynamic route)
- `pages/inventory/[id]/edit.vue` → `/inventory/:id/edit`

### Creating a New Page

1. Create a Vue file in `app/pages/`
2. Use the `<template>` for markup
3. Use `<script setup>` for logic (Composition API)
4. No import needed - the page is auto-registered

Example:
```vue
<script setup lang="ts">
const items = ref([])

onMounted(async () => {
  const { data } = await $fetch('/db/parts/')
  items.value = data
})
</script>

<template>
  <div>
    <h1>Parts List</h1>
    <div v-for="item in items" :key="item.id">
      {{ item.name }}
    </div>
  </div>
</template>
```

### Creating Components

Components in `app/components/` are auto-imported:

```vue
<!-- app/components/StatusBadge.vue -->
<script setup lang="ts">
defineProps<{
  status: string
}>()
</script>

<template>
  <UBadge :color="status === 'active' ? 'green' : 'gray'">
    {{ status }}
  </UBadge>
</template>
```

Use it anywhere without importing:
```vue
<StatusBadge status="active" />
```

### State Management

For simple state, use Nuxt's `useState`:

```typescript
// In any component or composable
const user = useState('user', () => ({ name: '', email: '' }))
```

For complex state, create a composable:

```typescript
// app/composables/useCart.ts
export const useCart = () => {
  const items = useState('cart-items', () => [])

  const addItem = (item) => {
    items.value.push(item)
  }

  const removeItem = (id) => {
    items.value = items.value.filter(i => i.id !== id)
  }

  return {
    items: readonly(items),
    addItem,
    removeItem
  }
}
```

## Testing

### Running Tests

```bash
# Run all tests
npm test

# Run unit tests only (Node environment)
npm run test:unit

# Run Nuxt integration tests (happy-dom environment)
npm run test:nuxt

# Watch mode
npm run test:watch
```

### Test Structure

Two test projects are configured in `vitest.config.ts`:

1. **unit**: For testing pure functions, utilities, and composables
2. **nuxt**: For testing Vue components with Nuxt context

### Writing Unit Tests

```typescript
// app/utils/formatCurrency.test.ts
import { describe, it, expect } from 'vitest'
import { formatCurrency } from './formatCurrency'

describe('formatCurrency', () => {
  it('formats USD correctly', () => {
    expect(formatCurrency(1234.56)).toBe('$1,234.56')
  })
})
```

### Writing Component Tests

```typescript
// app/components/StatusBadge.test.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import StatusBadge from './StatusBadge.vue'

describe('StatusBadge', () => {
  it('renders active status', () => {
    const wrapper = mount(StatusBadge, {
      props: { status: 'active' }
    })
    expect(wrapper.text()).toBe('active')
  })
})
```

## Coding Conventions

### TypeScript
- Use TypeScript for all new code
- Define prop types with `defineProps<T>()`
- Use type inference where possible
- Avoid `any` - use `unknown` if type is truly unknown

### Component Naming
- PascalCase for component files: `StatusBadge.vue`
- Use multi-word names to avoid conflicts with HTML elements
- Group related components in folders: `components/Dashboard/`

### Composition API
- Use `<script setup>` syntax
- Prefer `const` over `let`
- Use `ref()` for primitives, `reactive()` for objects (or just `ref()` for consistency)
- Destructure props with `defineProps()`

### Styling
- Use Tailwind utility classes for styling
- Prefer Nuxt UI components over custom components
- Use Tailwind's responsive modifiers: `md:`, `lg:`, etc.
- Extract common patterns to components, not CSS classes

### Code Organization
```vue
<script setup lang="ts">
// 1. Imports (if needed - most are auto-imported)
import { someExternalLib } from 'external-lib'

// 2. Props & Emits
const props = defineProps<{ id: string }>()
const emit = defineEmits<{ save: [data: any] }>()

// 3. Composables
const route = useRoute()
const router = useRouter()

// 4. State
const isLoading = ref(false)
const data = ref(null)

// 5. Computed
const displayName = computed(() => data.value?.name || 'Unknown')

// 6. Methods
const fetchData = async () => {
  isLoading.value = true
  // ... fetch logic
  isLoading.value = false
}

// 7. Lifecycle hooks
onMounted(() => {
  fetchData()
})
</script>

<template>
  <!-- Template here -->
</template>
```

## Component Development

### Using Nuxt UI Components

Nuxt UI components are prefixed with `U`:

```vue
<template>
  <UButton @click="handleClick">Click Me</UButton>

  <UInput v-model="search" placeholder="Search..." />

  <UTable :rows="items" :columns="columns" />

  <UModal v-model="isOpen">
    <UCard>
      <p>Modal content</p>
    </UCard>
  </UModal>
</template>
```

### Form Handling

```vue
<script setup lang="ts">
const form = ref({
  name: '',
  email: '',
  quantity: 0
})

const handleSubmit = async () => {
  const { data } = await $fetch('/db/parts/', {
    method: 'POST',
    body: form.value
  })
  navigateTo(`/parts/${data.id}`)
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <UInput v-model="form.name" label="Name" required />
    <UInput v-model="form.email" type="email" label="Email" />
    <UInput v-model.number="form.quantity" type="number" label="Quantity" />
    <UButton type="submit">Submit</UButton>
  </form>
</template>
```

## API Integration

### Using $fetch

Nuxt provides `$fetch` for API calls with automatic request/response handling:

```typescript
// GET request
const { data } = await $fetch('/db/parts/')

// POST request
const newPart = await $fetch('/db/parts/', {
  method: 'POST',
  body: { name: 'Resistor', value: '10k' }
})

// PUT request
await $fetch(`/db/parts/${id}`, {
  method: 'PUT',
  body: updatedData
})

// DELETE request
await $fetch(`/db/parts/${id}`, {
  method: 'DELETE'
})
```

### Error Handling

```typescript
const fetchPart = async (id: string) => {
  try {
    const part = await $fetch(`/db/parts/${id}`)
    return part
  } catch (error) {
    console.error('Failed to fetch part:', error)
    // Show user-friendly error
    useToast().add({
      title: 'Error',
      description: 'Failed to load part',
      color: 'red'
    })
  }
}
```

### Using useFetch for SSR

For data that should be fetched during SSR:

```typescript
const { data: parts, pending, error } = await useFetch('/db/parts/')
```

## Common Tasks

### Adding a New Route

1. Create file in `app/pages/`:
   ```bash
   touch app/pages/newpage.vue
   ```

2. Add component structure:
   ```vue
   <script setup lang="ts">
   // Your logic
   </script>

   <template>
     <div>
       <h1>New Page</h1>
     </div>
   </template>
   ```

3. Navigate to `/newpage`

### Creating a Reusable Composable

```typescript
// app/composables/useApiData.ts
export const useApiData = <T>(endpoint: string) => {
  const data = ref<T | null>(null)
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const fetch = async () => {
    loading.value = true
    error.value = null
    try {
      data.value = await $fetch(endpoint)
    } catch (e) {
      error.value = e as Error
    } finally {
      loading.value = false
    }
  }

  return { data, loading, error, fetch }
}
```

### Adding Global CSS

Add to `app/assets/css/main.css`:

```css
@import "tailwindcss";

/* Custom styles */
.custom-class {
  @apply bg-blue-500 text-white;
}
```

### Debugging

Use Vue DevTools browser extension for:
- Component inspection
- State management
- Performance profiling
- Route inspection

---

For more information:
- [Nuxt Documentation](https://nuxt.com/docs)
- [Vue 3 Documentation](https://vuejs.org/)
- [Nuxt UI Documentation](https://ui.nuxt.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
