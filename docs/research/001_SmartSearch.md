# Typesense + Django + FastAPI + Nuxt + InstantSearchJS Integration Research

## Executive Summary

Integrating Typesense with your Django/FastAPI/Nuxt stack is architecturally sound and well-supported. The key is establishing a proper data sync pipeline from Django → Typesense, then exposing search via FastAPI endpoints to your Nuxt frontend with instantsearchjs.

**Architecture Overview:**
```
Django (Primary DB) → Typesense (Search Index) ← FastAPI (Search API) ← Nuxt + InstantSearchJS (Frontend)
```

---

## 1. Current Ecosystem & Options

### Available Django Integration

**django-typesense** (Siege-Software)
- **Status:** Alpha (pip package available, actively maintained on GitHub)
- **Last Release:** May 2024
- **Features:**
  - Automatic model-to-Typesense collection mapping via declarative Collections
  - Django ORM signal hooks (post_save, pre_delete, m2m_changed) for real-time indexing
  - QuerySet.update() override for batch updates
  - Django Admin integration with TypesenseSearchAdminMixin
  - Bulk indexing utilities
  - Synonym management

**Installation:**
```bash
pip install django-typesense
# or latest from GitHub
pip install git+https://github.com/Siege-Software/django-typesense.git
```

### InstantSearchJS & Vue/Nuxt Integration

**vue-instantsearch** (Algolia's Vue component library)
- Works with Typesense via custom adapter
- Provides pre-built UI components (search box, hits, refinements, pagination)
- Vue 3 compatible
- Can be used in Nuxt 3 projects

**@nuxtjs/algolia** (Nuxt module)
- Direct Nuxt integration
- Supports vue-instantsearch components
- Composables: `useAlgoliaSearch`, `useAsyncAlgoliaSearch`
- Can be adapted for Typesense with custom client

**Installation (Nuxt 4):**
```bash
npm install instantsearch.js instantsearch.css vue-instantsearch
```

---

## 2. Django → Typesense Data Sync Strategies

### A. ORM Hook-Based Sync (Recommended for Real-Time)

**How it works:**
- django-typesense listens to Django signals (post_save, pre_delete, m2m_changed)
- Changes are captured immediately and pushed to Typesense
- Best for moderate-volume applications

**Implementation:**
```python
# models.py
from django_typesense.mixins import TypesenseModelMixin

class Song(TypesenseModelMixin):
    title = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    artists = models.ManyToManyField(Artist)
    number_of_views = models.IntegerField(default=0)
    duration = models.DurationField()
    description = models.TextField()
    
    collection_class = SongCollection

# collections.py
from django_typesense.collections import TypesenseCollection
from django_typesense import fields

class SongCollection(TypesenseCollection):
    query_by_fields = 'title,artist_names,genre_name'  # Required
    
    title = fields.TypesenseCharField()
    genre_name = fields.TypesenseCharField(value='genre.name')
    genre_id = fields.TypesenseSmallIntegerField()
    artist_names = fields.TypesenseArrayField(
        base_field=fields.TypesenseCharField(), 
        value='artist_names'
    )
    number_of_views = fields.SmallIntegerField(index=False)
    duration = fields.DurationField()
    description = fields.TypesenseCharField()

# When you save a Song, it automatically syncs to Typesense
song = Song.objects.create(title="Example", ...)  # ✅ Auto-synced
song.title = "Updated"
song.save()  # ✅ Auto-synced
```

**Pros:**
- Zero additional infrastructure
- Real-time updates
- Automatic signal handling
- Built-in bulk indexing utilities

**Cons:**
- Blocks save operations (minimal impact with Typesense's speed)
- Single-threaded by default
- Can cause cascading failures if Typesense is down

### B. Buffering Strategy (Recommended for High Volume)

**How it works:**
1. Changes written to a "sync buffer" table in Django DB
2. Async job polls buffer every 5-10s and bulk imports to Typesense
3. Decouples Django saves from Typesense indexing

**Implementation:**
```python
# models.py
class TypesenseSyncBuffer(models.Model):
    OPERATION_CHOICES = (
        ('insert', 'Insert'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    )
    
    record_id = models.IntegerField()
    model_name = models.CharField(max_length=100)  # 'Song', 'Artist', etc.
    operation_type = models.CharField(max_length=10, choices=OPERATION_CHOICES)
    record_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

# tasks.py (Celery or APScheduler)
from django_typesense.utils import bulk_update_typesense_records
from .models import TypesenseSyncBuffer, Song

@app.task
def sync_typesense_buffer():
    """Run every 5-10 seconds"""
    unprocessed = TypesenseSyncBuffer.objects.filter(processed=False)
    
    if not unprocessed.exists():
        return
    
    for buffer_record in unprocessed:
        if buffer_record.model_name == 'Song':
            song = Song.objects.get(id=buffer_record.record_id)
            if buffer_record.operation_type in ['insert', 'update']:
                collection = SongCollection([song], many=False)
                collection.update()
            elif buffer_record.operation_type == 'delete':
                # Handle deletion via Typesense API
                typesense_client.collections['songs'].documents[str(buffer_record.record_id)].delete()
        
        buffer_record.processed = True
        buffer_record.save()
```

**Pros:**
- Non-blocking writes
- Efficient bulk imports
- Audit trail of changes
- Handles high volume (10s+ writes/sec)

**Cons:**
- ~5-10s eventual consistency
- Additional infrastructure (task queue)

### C. Polling Strategy (For Periodic Sync)

**How it works:**
1. Track `updated_at` timestamps on models
2. Periodically query for records changed since last sync
3. Bulk import changes

**Implementation:**
```python
# Configuration
TYPESENSE = {
    "api_key": os.getenv('TYPESENSE_API_KEY'),
    "nodes": [{
        "host": os.getenv('TYPESENSE_HOST', 'localhost'),
        "port": os.getenv('TYPESENSE_PORT', '8108'),
        "protocol": os.getenv('TYPESENSE_PROTOCOL', 'http'),
    }],
    "connection_timeout_seconds": 2,
}

# Periodic task (runs every 30s)
@app.task
def sync_typesense_periodic():
    last_sync = SyncMetadata.objects.filter(model='Song').first()
    last_synced_at = last_sync.last_synced_at if last_sync else timezone.now()
    
    # Find records updated since last sync
    updated_songs = Song.objects.filter(updated_at__gte=last_synced_at)
    
    if updated_songs.exists():
        bulk_update_typesense_records(updated_songs, batch_size=1024)
        
        SyncMetadata.objects.update_or_create(
            model='Song',
            defaults={'last_synced_at': timezone.now()}
        )
```

**Pros:**
- Simple to implement
- No signal overhead
- Controlled sync frequency

**Cons:**
- Maximum 30s+ lag
- Requires timestamp fields
- Doesn't catch soft-deletes automatically

---

## 3. FastAPI Search Endpoint Setup

### Basic FastAPI Search Wrapper

```python
# fastapi_app/search.py
from fastapi import FastAPI, Query
from typesense import Client
import os

app = FastAPI()

# Initialize Typesense client
typesense_client = Client({
    'api_key': os.getenv('TYPESENSE_API_KEY'),
    'nodes': [{
        'host': os.getenv('TYPESENSE_HOST', 'localhost'),
        'port': int(os.getenv('TYPESENSE_PORT', 8108)),
        'protocol': os.getenv('TYPESENSE_PROTOCOL', 'http'),
    }],
    'connection_timeout_seconds': 2,
})

@app.get('/api/search/songs')
async def search_songs(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    filter_by: str = Query(None),  # e.g., "number_of_views:>100"
    facet_by: str = Query(None),  # e.g., "genre_name"
):
    """
    Search songs via Typesense
    
    Examples:
        /api/search/songs?q=love
        /api/search/songs?q=love&filter_by=duration:[0..200]
        /api/search/songs?q=love&facet_by=genre_name
    """
    try:
        search_parameters = {
            'q': q,
            'query_by': 'title,artist_names,genre_name,description',
            'limit': limit,
            'offset': offset,
        }
        
        if filter_by:
            search_parameters['filter_by'] = filter_by
        
        if facet_by:
            search_parameters['facet_by'] = facet_by
        
        results = typesense_client.collections['songs'].documents.search(
            search_parameters
        )
        
        return {
            'status': 'success',
            'data': results,
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
        }

@app.get('/api/search/suggestions')
async def search_suggestions(
    q: str = Query(..., min_length=1),
    limit: int = Query(5, ge=1, le=20),
):
    """Autocomplete suggestions"""
    try:
        results = typesense_client.collections['songs'].documents.search({
            'q': q,
            'query_by': 'title,artist_names',
            'limit': limit,
            'prefix': 'true',
            'drop_tokens_threshold': 0,
        })
        
        # Extract just titles for autocomplete
        suggestions = [
            hit['document']['title'] 
            for hit in results.get('hits', [])
        ]
        
        return {'suggestions': suggestions}
    
    except Exception as e:
        return {'error': str(e)}
```

### CORS Configuration

```python
# main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'https://yourdomain.com'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
```

---

## 4. Nuxt + InstantSearchJS Frontend Implementation

### Option A: Using vue-instantsearch (Component-Based)

```vue
<!-- pages/search.vue -->
<template>
  <div class="search-container">
    <ais-instant-search
      :search-client="searchClient"
      index-name="songs"
    >
      <!-- Search Box -->
      <div class="search-box-wrapper">
        <ais-search-box 
          placeholder="Search songs, artists, genres..."
          autofocus
        />
      </div>

      <!-- Results -->
      <div class="results-grid">
        <ais-hits>
          <template v-slot="{ items }">
            <div 
              v-for="item in items" 
              :key="item.id"
              class="result-card"
            >
              <h3>{{ item.title }}</h3>
              <p class="artists">{{ item.artist_names.join(', ') }}</p>
              <p class="genre">{{ item.genre_name }}</p>
              <p class="views">👁️ {{ item.number_of_views }} views</p>
            </div>
          </template>
        </ais-hits>
      </div>

      <!-- Facets -->
      <div class="facets">
        <ais-refinement-list attribute="genre_name" />
      </div>

      <!-- Pagination -->
      <ais-pagination />
    </ais-instant-search>
  </div>
</template>

<script setup lang="ts">
import { 
  AisInstantSearch, 
  AisSearchBox, 
  AisHits,
  AisRefinementList,
  AisPagination,
} from 'vue-instantsearch/vue3/es'
import { instantMeiliSearch } from '@meilisearch/instant-meilisearch'
import 'instantsearch.css/themes/algolia-min.css'

// Custom Typesense adapter
const searchClient = {
  search: async (requests) => {
    return Promise.all(
      requests.map(async (request) => {
        const response = await fetch(`/api/search/songs?q=${encodeURIComponent(request.params.query)}&limit=${request.params.hitsPerPage || 10}&offset=${(request.params.page || 0) * (request.params.hitsPerPage || 10)}`)
        const data = await response.json()
        
        return {
          hits: data.data.hits?.map(h => h.document) || [],
          nbHits: data.data.found,
          page: request.params.page || 0,
          nbPages: Math.ceil((data.data.found || 0) / (request.params.hitsPerPage || 10)),
        }
      })
    )
  }
}
</script>

<style scoped>
.search-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.search-box-wrapper {
  margin-bottom: 2rem;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.result-card {
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s;
}

.result-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.result-card h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.artists {
  color: #666;
  font-size: 0.9rem;
  margin: 0.25rem 0;
}

.genre {
  color: #999;
  font-size: 0.85rem;
  margin: 0.25rem 0;
}

.views {
  color: #bbb;
  font-size: 0.8rem;
  margin-top: 0.5rem;
}

.facets {
  position: fixed;
  left: 0;
  top: 100px;
  width: 200px;
  padding: 1rem;
  border-right: 1px solid #e0e0e0;
}
</style>
```

### Option B: Custom Hook-Based Implementation (More Control)

```vue
<!-- composables/useTypesenseSearch.ts -->
export const useTypesenseSearch = () => {
  const results = ref([])
  const loading = ref(false)
  const facets = ref({})
  const totalHits = ref(0)
  
  const search = async (query, options = {}) => {
    loading.value = true
    
    try {
      const params = new URLSearchParams({
        q: query,
        limit: options.limit || 20,
        offset: options.offset || 0,
        ...(options.filterBy && { filter_by: options.filterBy }),
        ...(options.facetBy && { facet_by: options.facetBy }),
      })
      
      const response = await fetch(`/api/search/songs?${params}`)
      const data = await response.json()
      
      results.value = data.data.hits?.map(h => h.document) || []
      totalHits.value = data.data.found
      facets.value = data.data.facet_counts || {}
      
    } catch (error) {
      console.error('Search error:', error)
    } finally {
      loading.value = false
    }
  }
  
  const getSuggestions = async (query) => {
    try {
      const response = await fetch(
        `/api/search/suggestions?q=${encodeURIComponent(query)}`
      )
      return response.json()
    } catch (error) {
      console.error('Suggestions error:', error)
      return []
    }
  }
  
  return {
    results: readonly(results),
    loading: readonly(loading),
    facets: readonly(facets),
    totalHits: readonly(totalHits),
    search,
    getSuggestions,
  }
}

<!-- pages/search.vue using hook -->
<template>
  <div class="search-page">
    <div class="search-header">
      <input
        v-model="query"
        type="text"
        placeholder="Search songs..."
        @input="handleSearch"
        class="search-input"
      />
    </div>
    
    <div v-if="loading" class="loading">Searching...</div>
    
    <div v-else class="results">
      <p class="hit-count">Found {{ totalHits }} results</p>
      
      <div class="results-list">
        <div 
          v-for="song in results" 
          :key="song.id"
          class="song-item"
        >
          <h4>{{ song.title }}</h4>
          <p>{{ song.artist_names?.join(', ') }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useTypesenseSearch } from '~/composables/useTypesenseSearch'

const query = ref('')
const { results, loading, totalHits, search } = useTypesenseSearch()

const handleSearch = async (event) => {
  const q = event.target.value
  if (q.length > 2) {
    await search(q)
  }
}
</script>
```

### nuxt.config.ts Configuration

```typescript
export default defineNuxtConfig({
  modules: [],
  
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000',
    },
  },
  
  ssr: true,
  
  nitro: {
    prerender: {
      crawlLinks: true,
      routes: ['/search'],
    },
  },
})
```

---

## 5. Typesense Configuration

### Docker Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  typesense:
    image: typesense/typesense:29.0
    ports:
      - "8108:8108"
    volumes:
      - typesense_data:/data
    environment:
      TYPESENSE_API_KEY: ${TYPESENSE_API_KEY:-your-secret-api-key}
      TYPESENSE_DATA_DIR: /data
      TYPESENSE_ENABLE_CORS: "true"
    command: --data-dir /data --api-key=${TYPESENSE_API_KEY:-your-secret-api-key}

volumes:
  typesense_data:
```

### Initial Collection Creation

```python
# Django management command: manage.py shell
from typesense import Client

client = Client({
    'api_key': 'your-secret-api-key',
    'nodes': [{'host': 'localhost', 'port': 8108, 'protocol': 'http'}],
})

# Create collection schema
schema = {
    'name': 'songs',
    'fields': [
        {'name': 'id', 'type': 'string'},
        {'name': 'title', 'type': 'string'},
        {'name': 'artist_names', 'type': 'string[]'},
        {'name': 'genre_name', 'type': 'string'},
        {'name': 'genre_id', 'type': 'int32'},
        {'name': 'number_of_views', 'type': 'int32', 'index': False},
        {'name': 'duration', 'type': 'int32'},
        {'name': 'description', 'type': 'string'},
        {'name': 'release_date', 'type': 'int64', 'optional': True},  # Unix timestamp
    ],
    'default_sorting_field': 'number_of_views',
}

client.collections.create(schema)
```

---

## 6. Data Sync to Typesense (Initial Population)

### Using django-typesense Bulk Import

```bash
# Django shell
from django.core.management import call_command
call_command('sync_typesense')
```

### Or via Python Script

```python
# scripts/sync_to_typesense.py
from django_typesense.utils import bulk_update_typesense_records
from myapp.models import Song
from myapp.collections import SongCollection

# Initial sync
songs = Song.objects.all().order_by('id')
bulk_update_typesense_records(songs, batch_size=1024)

print(f"Synced {songs.count()} songs to Typesense")
```

---

## 7. Complete Architecture Diagram

```
┌─────────────────┐
│   Django App    │
│   (Primary DB)  │
└────────┬────────┘
         │
         │ (1) ORM Signal Hooks
         │     or Polling Job
         │
         ↓
┌─────────────────────────────┐
│  Typesense Search Index     │
│  Collections:               │
│  - songs                    │
│  - artists                  │
│  - genres                   │
└────────┬────────────────────┘
         │
         │ (2) REST API Queries
         │     /api/search/songs
         │
         ↓
┌──────────────────────────────┐
│   FastAPI Search Layer       │
│   - Query routing            │
│   - Pagination               │
│   - Filtering/Faceting       │
│   - Response formatting      │
└──────────┬───────────────────┘
           │
           │ (3) JSON Responses
           │
           ↓
┌──────────────────────────────┐
│  Nuxt Frontend               │
│  - vue-instantsearch         │
│  - Custom search composable  │
│  - Autocomplete              │
│  - Results display           │
└──────────────────────────────┘
```

---

## 8. Performance Considerations

### Indexing Performance
- **django-typesense bulk import:** 1,000+ docs/sec on standard hardware
- **Single-document indexing:** ~100 docs/sec
- **For high volume (10s+ writes/sec):** Use buffer + bulk import strategy

### Search Performance
- **Latency:** 10-50ms for typical queries (depends on query complexity)
- **Throughput:** Easily handles 100+ QPS on moderate hardware
- **Optimization tips:**
  - Mark display-only fields as `index: False`
  - Use `prefix: 'true'` for autocomplete
  - Implement caching for common queries

### Disk & Memory
- **Memory usage:** Proportional to indexed data
- **Disk usage:** 5-10x the source data size (includes indexes)
- **Typesense Cloud default:** 5X disk provisioning vs RAM

---

## 9. Error Handling & Monitoring

### Handling Sync Failures

```python
# tasks.py
@app.task(bind=True, max_retries=3)
def sync_to_typesense_with_retry(self, song_id):
    try:
        song = Song.objects.get(id=song_id)
        collection = SongCollection([song], many=False)
        collection.update()
    except Exception as exc:
        # Retry with exponential backoff
        retry_delay = 2 ** self.request.retries
        raise self.retry(exc=exc, countdown=retry_delay)
```

### Monitoring Sync Status

```python
# models.py
class SyncLog(models.Model):
    model_name = models.CharField(max_length=100)
    record_id = models.IntegerField()
    status = models.CharField(
        max_length=20, 
        choices=[('pending', 'Pending'), ('synced', 'Synced'), ('failed', 'Failed')]
    )
    error_message = models.TextField(blank=True)
    synced_at = models.DateTimeField(null=True)
```

---

## 10. Recommended Implementation Roadmap

### Phase 1: Basic Setup (Week 1)
1. ✅ Install `django-typesense`
2. ✅ Define Collections for your Django models
3. ✅ Create FastAPI search endpoint
4. ✅ Initial bulk import to Typesense
5. ✅ Test Django → Typesense sync via signal hooks

### Phase 2: Frontend Integration (Week 2)
1. ✅ Add `vue-instantsearch` to Nuxt
2. ✅ Create search page with results display
3. ✅ Implement autocomplete suggestions
4. ✅ Add filtering/faceting UI

### Phase 3: Production Hardening (Week 3)
1. ✅ Implement buffer-based sync for high-volume scenarios
2. ✅ Add error handling & monitoring
3. ✅ Performance testing & optimization
4. ✅ Typesense Cloud deployment (or self-hosted HA setup)

### Phase 4: Advanced Features (Week 4+)
1. ✅ Vector/semantic search if needed
2. ✅ Custom ranking/merchandising
3. ✅ Analytics/search insights
4. ✅ Multi-language support via Typesense localization

---

## 11. Useful Resources

- **Typesense Docs:** https://typesense.org/docs/
- **django-typesense GitHub:** https://github.com/Siege-Software/django-typesense
- **Typesense API Reference:** https://typesense.org/docs/29.0/api/
- **vue-instantsearch:** https://www.algolia.com/doc/guides/building-search-ui/installation/vue/
- **Typesense Python Client:** https://github.com/typesense/typesense-python
- **InstantSearch.js:** https://www.algolia.com/doc/guides/building-search-ui/installation/js/

---

## 12. Potential Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Typesense down → Django saves blocked | Buffer strategy + async sync |
| Schema mismatches between Django & Typesense | Use django-typesense Collections |
| High memory usage at scale | Exclude non-indexed fields, use Typesense Cloud |
| Complex queries (JOINs, nested filters) | Pre-compute in Django, denormalize in Typesense |
| Autocomplete latency | Use `prefix: 'true'` + query caching |
| Pagination with filters | Typesense supports offset/limit + filter_by natively |
| Real-time collaboration conflicts | Track update timestamps, implement conflict resolution |

---

## Summary

Your stack is well-positioned for this integration:

✅ **django-typesense** provides seamless Django ORM integration  
✅ **FastAPI** can expose Typesense as a REST API  
✅ **InstantSearchJS + vue-instantsearch** provide battle-tested UI components  
✅ **Nuxt** provides the framework for responsive search UX

The main decision point is sync strategy (real-time signals vs. buffered batch vs. polling) 
based on your write volume and latency requirements. For this project, signal-based sync is 
appropriate.
