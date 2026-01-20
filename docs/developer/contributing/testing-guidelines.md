# Testing Guidelines

## Backend Testing

All backend changes should include appropriate tests:

```python
# backend/tests/test_feature.py
import pytest
from parts.models import Part

@pytest.mark.django_db
class TestNewFeature:
    def test_feature_works(self):
        # Arrange
        part = Part.objects.create(name="Test Part")

        # Act
        result = part.some_method()

        # Assert
        assert result == expected_value
```

**Test Coverage Requirements:**
- New features must have tests
- Bug fixes should include regression tests
- Aim for >80% code coverage

## Frontend Testing

Frontend changes should include component and unit tests:

```typescript
// app/components/NewComponent.test.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import NewComponent from './NewComponent.vue'

describe('NewComponent', () => {
  it('renders correctly', () => {
    const wrapper = mount(NewComponent, {
      props: { title: 'Test' }
    })
    expect(wrapper.text()).toContain('Test')
  })
})
```

## Running Tests Locally

Always run tests before submitting a PR:

```bash
# Backend
uv run pytest -v

# Frontend
cd frontend
npm test

# Run both
uv run pytest && cd frontend && npm test
```
