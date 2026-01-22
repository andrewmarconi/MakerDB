# Development Workflow

## File-based Routing
Nuxt uses file-based routing. Pages are automatically generated based on the file structure in `app/pages/`:

- `pages/index.vue` → `/`
- `pages/inventory/index.vue` → `/inventory`
- `pages/inventory/[id]/index.vue` → `/inventory/:id` (dynamic route)
- `pages/inventory/[id]/edit.vue` → `/inventory/:id/edit`

## Creating a New Page

1. Create a Vue file in `app/pages/`
2. Use the `<template>` for markup
3. Use `<script setup lang="ts">` for logic (Composition API)
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

## Creating Components

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

## State Management

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
