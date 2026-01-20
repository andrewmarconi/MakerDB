# Common Tasks

## Adding a New Route

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

## Creating a Reusable Composable

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

## Adding Global CSS

Add to `app/assets/css/main.css`:

```css
@import "tailwindcss";

/* Custom styles */
.custom-class {
  @apply bg-blue-500 text-white;
}
```

## Debugging

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
