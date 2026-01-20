# API Integration

## Using $fetch

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

## Error Handling

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

## Using useFetch for SSR

For data that should be fetched during SSR:

```typescript
const { data: parts, pending, error } = await useFetch('/db/parts/')
```
