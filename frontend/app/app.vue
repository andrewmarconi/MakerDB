<script setup lang="ts">
useSeoMeta({
  titleTemplate: '%s | MakerDB',
  description: 'MakerDB - A comprehensive database for managing electronic components, projects, and production costs.',
  ogDescription: 'MakerDB - A comprehensive database for managing electronic components, projects, and production costs.',
  ogSiteName: 'MakerDB',
  twitterCard: 'summary_large_image'
})
</script>

<template>
  <UApp>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
    <UToaster />
  </UApp>
</template>
