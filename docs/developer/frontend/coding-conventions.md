# Coding Conventions

## TypeScript
- Use TypeScript for all new code
- Define prop types with `defineProps<T>()`
- Use type inference where possible
- Avoid `any` - use `unknown` if type is truly unknown

## Component Naming
- PascalCase for component files: `StatusBadge.vue`
- Use multi-word names to avoid conflicts with HTML elements
- Group related components in folders: `components/Dashboard/`

## Composition API
- Use `<script setup lang="ts">` syntax
- Prefer `const` over `let`
- Use `ref()` for primitives, `reactive()` for objects (or just `ref()` for consistency)
- Destructure props with `defineProps()`

## Styling
- Use Tailwind utility classes for styling
- Prefer Nuxt UI components over custom components
- Use Tailwind's responsive modifiers: `md:`, `lg:`, etc.
- Extract common patterns to components, not CSS classes

## Code Organization
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
