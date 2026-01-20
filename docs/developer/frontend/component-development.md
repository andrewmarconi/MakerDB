# Component Development

## Using Nuxt UI Components

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

## Form Handling

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
