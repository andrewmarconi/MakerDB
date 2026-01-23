export interface SearchHit {
  id: string
  name: string
  description: string
  parent_id: string
  created_at: number
}

export interface SearchResult {
  hits: SearchHit[]
}

export const useSmartSearch = () => {
  const results = ref<SearchHit[]>([])
  const loading = ref(false)
  const query = ref('')

  const search = async (searchQuery: string, entity: string = 'locations') => {
    if (!searchQuery || searchQuery.length < 2) {
      results.value = []
      query.value = ''
      return
    }

    query.value = searchQuery
    loading.value = true

    try {
      const data = await useApiFetch<SearchResult>(`/api/search/${entity}?q=${encodeURIComponent(searchQuery)}`)
      results.value = data.hits || []
    } catch (e) {
      console.error('Search error:', e)
      results.value = []
    } finally {
      loading.value = false
    }
  }

  const clear = () => {
    results.value = []
    query.value = ''
  }

  return {
    results: readonly(results),
    loading: readonly(loading),
    query: readonly(query),
    search,
    clear
  }
}
