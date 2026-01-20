# Testing

## Running Tests

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

## Test Structure

Two test projects are configured in `vitest.config.ts`:

1. **unit**: For testing pure functions, utilities, and composables
2. **nuxt**: For testing Vue components with Nuxt context

## Writing Unit Tests

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

## Writing Component Tests

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
