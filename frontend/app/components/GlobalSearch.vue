<script setup lang="ts">
import { useSmartSearch } from '~/composables/useSmartSearch'
import { useDebounceFn, onClickOutside } from '@vueuse/core'

const { results, loading, query, search, clear } = useSmartSearch()
const inputRef = ref<HTMLInputElement | null>(null)
const showResults = ref(false)
const searchQuery = ref('')

const debouncedSearch = useDebounceFn((q: string) => {
  search(q)
  showResults.value = q.length >= 2
}, 150)

function handleInput() {
  if (searchQuery.value.length < 2) {
    clear()
    showResults.value = false
    return
  }
  debouncedSearch(searchQuery.value)
}

function handleFocus() {
  if (searchQuery.value.length >= 2 && results.value.length > 0) {
    showResults.value = true
  }
}

function handleBlur() {
  setTimeout(() => {
    showResults.value = false
  }, 200)
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') {
    showResults.value = false
    inputRef.value?.blur()
  }
}

onMounted(() => {
  const handleGlobalKeydown = (e: KeyboardEvent) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault()
      inputRef.value?.focus()
    }
  }
  window.addEventListener('keydown', handleGlobalKeydown)
  onUnmounted(() => window.removeEventListener('keydown', handleGlobalKeydown))
})

const resultCount = computed(() => results.value.length)
</script>

<template>
  <div class="relative">
    <UInput
      ref="inputRef"
      v-model="searchQuery"
      icon="i-heroicons-magnifying-glass"
      placeholder="Search locations..."
      autocomplete="off"
      class="w-72"
      @input="handleInput"
      @focus="handleFocus"
      @blur="handleBlur"
      @keydown="handleKeydown"
    >
      <template #trailing>
        <UKbd class="hidden sm:flex">⌘</UKbd>
        <UKbd class="hidden sm:flex">K</UKbd>
      </template>
    </UInput>

    <!-- Results dropdown -->
    <Transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 translate-y-1"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 translate-y-1"
    >
      <div
        v-if="showResults && results.length > 0"
        class="absolute right-0 top-full mt-2 w-96 bg-white dark:bg-gray-900 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-50 overflow-hidden"
      >
        <div class="px-4 py-2 border-b border-gray-200 dark:border-gray-700 text-xs text-gray-500 flex justify-between">
          <span>{{ resultCount }} result{{ resultCount !== 1 ? 's' : '' }}</span>
          <span class="text-gray-400">Locations</span>
        </div>

        <ul class="max-h-96 overflow-y-auto">
          <li v-for="hit in results" :key="hit.id">
            <NuxtLink
              :to="`/locations/${hit.id}`"
              class="block px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
              @click="showResults = false"
            >
              <div class="flex items-center justify-between">
                <div class="flex-1 min-w-0">
                  <p class="font-medium text-gray-900 dark:text-gray-100 truncate">{{ hit.name }}</p>
                  <p v-if="hit.description" class="text-sm text-gray-500 dark:text-gray-400 truncate">
                    {{ hit.description }}
                  </p>
                </div>
                <UIcon
                  name="i-heroicons-chevron-right"
                  class="w-4 h-4 text-gray-400 ml-2 flex-shrink-0"
                />
              </div>
            </NuxtLink>
          </li>
        </ul>

        <div v-if="loading" class="px-4 py-3 text-center text-gray-500 text-sm">
          <UIcon name="i-heroicons-arrow-path" class="w-4 h-4 animate-spin mx-auto" />
          <span class="mt-1 block">Searching...</span>
        </div>
      </div>
    </Transition>

    <!-- No results state -->
    <Transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 translate-y-1"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 translate-y-1"
    >
      <div
        v-if="showResults && searchQuery.length >= 2 && results.length === 0 && !loading"
        class="absolute right-0 top-full mt-2 w-72 bg-white dark:bg-gray-900 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-50 p-4 text-center"
      >
        <UIcon name="i-heroicons-magnifying-glass" class="w-8 h-8 text-gray-400 mx-auto mb-2" />
        <p class="text-gray-500 dark:text-gray-400">No locations found for "{{ searchQuery }}"</p>
      </div>
    </Transition>
  </div>
</template>
