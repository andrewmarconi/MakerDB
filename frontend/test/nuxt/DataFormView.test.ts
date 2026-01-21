import { describe, expect, it, vi, beforeEach, afterEach } from 'vitest'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import DataFormView from '~/components/DataFormView.vue'
import DataFormField from '~/components/DataFormField.vue'
import type { FieldSchema } from '~/shared/types/ui'

// Mock $fetch
const mockFetch = vi.fn()
vi.stubGlobal('$fetch', mockFetch)

describe('DataFormView', () => {
  const basicSchema: FieldSchema[] = [
    { key: 'name', label: 'Name', type: 'text', required: true },
    { key: 'description', label: 'Description', type: 'textarea' },
    { key: 'count', label: 'Count', type: 'number' },
    { key: 'active', label: 'Active', type: 'checkbox' },
  ]

  const basicModelValue = {
    name: 'Test Item',
    description: 'A test description',
    count: 5,
    active: true,
  }

  beforeEach(() => {
    mockFetch.mockReset()
    mockFetch.mockResolvedValue({ success: true })
  })

  afterEach(() => {
    vi.clearAllMocks()
  })

  it('renders fields from schema', async () => {
    const wrapper = await mountSuspended(DataFormView, {
      props: {
        modelValue: basicModelValue,
        schema: basicSchema,
        endpoint: '/api/items',
        entityId: '123',
      },
    })

    // Should render all field labels
    expect(wrapper.text()).toContain('Name')
    expect(wrapper.text()).toContain('Description')
    expect(wrapper.text()).toContain('Count')
    expect(wrapper.text()).toContain('Active')

    // Should show field values
    expect(wrapper.text()).toContain('Test Item')
    expect(wrapper.text()).toContain('A test description')
    expect(wrapper.text()).toContain('5')
    expect(wrapper.text()).toContain('Yes') // checkbox displays as Yes/No
  })

  it('displays empty placeholder for empty values', async () => {
    const wrapper = await mountSuspended(DataFormView, {
      props: {
        modelValue: { name: '', description: null, count: undefined, active: false },
        schema: basicSchema,
        endpoint: '/api/items',
        entityId: '123',
      },
    })

    // Should display em-dash for empty values
    expect(wrapper.text()).toContain('—')
    // Checkbox false should show "No"
    expect(wrapper.text()).toContain('No')
  })

  it('applies two-column layout when specified', async () => {
    const wrapper = await mountSuspended(DataFormView, {
      props: {
        modelValue: basicModelValue,
        schema: basicSchema,
        endpoint: '/api/items',
        entityId: '123',
        layout: 'two-column',
      },
    })

    const container = wrapper.find('div')
    expect(container.classes()).toContain('grid')
    expect(container.classes()).toContain('md:grid-cols-2')
  })

  it('respects readonly prop', async () => {
    const wrapper = await mountSuspended(DataFormView, {
      props: {
        modelValue: basicModelValue,
        schema: basicSchema,
        endpoint: '/api/items',
        entityId: '123',
        readonly: true,
      },
    })

    const fieldComponents = wrapper.findAllComponents(DataFormField)
    fieldComponents.forEach(field => {
      expect(field.props('readonly')).toBe(true)
    })
  })

  it('marks required fields with asterisk', async () => {
    const wrapper = await mountSuspended(DataFormView, {
      props: {
        modelValue: basicModelValue,
        schema: basicSchema,
        endpoint: '/api/items',
        entityId: '123',
      },
    })

    // The Name field is required, should have asterisk
    const html = wrapper.html()
    expect(html).toContain('*')
  })
})

describe('DataFormField', () => {
  it('enters edit mode on click', async () => {
    const wrapper = await mountSuspended(DataFormField, {
      props: {
        schema: { key: 'name', label: 'Name', type: 'text' },
        modelValue: 'Test',
        state: 'idle',
      },
    })

    // Click the field display area (not tags type, so it's the clickable div)
    const displayArea = wrapper.find('.min-h-\\[2\\.5rem\\]')
    await displayArea.trigger('click')

    // Should emit focus event
    expect(wrapper.emitted('focus')).toBeTruthy()
  })

  it('does not enter edit mode when readonly', async () => {
    const wrapper = await mountSuspended(DataFormField, {
      props: {
        schema: { key: 'name', label: 'Name', type: 'text' },
        modelValue: 'Test',
        state: 'idle',
        readonly: true,
      },
    })

    await wrapper.find('.group').trigger('click')
    expect(wrapper.emitted('focus')).toBeFalsy()
  })

  it('does not enter edit mode when field schema is readonly', async () => {
    const wrapper = await mountSuspended(DataFormField, {
      props: {
        schema: { key: 'name', label: 'Name', type: 'text', readonly: true },
        modelValue: 'Test',
        state: 'idle',
      },
    })

    await wrapper.find('.group').trigger('click')
    expect(wrapper.emitted('focus')).toBeFalsy()
  })

  it('shows input when in editing state', async () => {
    const wrapper = await mountSuspended(DataFormField, {
      props: {
        schema: { key: 'name', label: 'Name', type: 'text' },
        modelValue: 'Test',
        state: 'editing',
      },
    })

    // Should show input element
    expect(wrapper.find('input').exists()).toBe(true)
  })

  it('shows textarea for textarea type', async () => {
    const wrapper = await mountSuspended(DataFormField, {
      props: {
        schema: { key: 'desc', label: 'Description', type: 'textarea' },
        modelValue: 'Test description',
        state: 'editing',
      },
    })

    expect(wrapper.find('textarea').exists()).toBe(true)
  })

  it('emits cancel on Escape key', async () => {
    const wrapper = await mountSuspended(DataFormField, {
      props: {
        schema: { key: 'name', label: 'Name', type: 'text' },
        modelValue: 'Test',
        state: 'editing',
      },
    })

    await wrapper.find('input').trigger('keydown', { key: 'Escape' })
    expect(wrapper.emitted('cancel')).toBeTruthy()
  })

  it('emits save on Enter key for text fields', async () => {
    const wrapper = await mountSuspended(DataFormField, {
      props: {
        schema: { key: 'name', label: 'Name', type: 'text' },
        modelValue: 'Test',
        state: 'editing',
      },
    })

    await wrapper.find('input').trigger('keydown', { key: 'Enter' })
    expect(wrapper.emitted('save')).toBeTruthy()
  })

  it('does not emit save on Enter for textarea fields', async () => {
    const wrapper = await mountSuspended(DataFormField, {
      props: {
        schema: { key: 'desc', label: 'Description', type: 'textarea' },
        modelValue: 'Test',
        state: 'editing',
      },
    })

    await wrapper.find('textarea').trigger('keydown', { key: 'Enter' })
    expect(wrapper.emitted('save')).toBeFalsy()
  })

  it('shows saving spinner when state is saving', async () => {
    const wrapper = await mountSuspended(DataFormField, {
      props: {
        schema: { key: 'name', label: 'Name', type: 'text' },
        modelValue: 'Test',
        state: 'saving',
      },
    })

    expect(wrapper.find('.animate-spin').exists()).toBe(true)
  })

  it('shows success checkmark when state is success', async () => {
    const wrapper = await mountSuspended(DataFormField, {
      props: {
        schema: { key: 'name', label: 'Name', type: 'text' },
        modelValue: 'Test',
        state: 'success',
      },
    })

    expect(wrapper.find('.text-green-500').exists()).toBe(true)
  })

  it('shows error message when provided', async () => {
    const wrapper = await mountSuspended(DataFormField, {
      props: {
        schema: { key: 'name', label: 'Name', type: 'text' },
        modelValue: 'Test',
        state: 'error',
        error: 'This field is required',
      },
    })

    expect(wrapper.text()).toContain('This field is required')
  })

  it('displays select options correctly', async () => {
    const wrapper = await mountSuspended(DataFormField, {
      props: {
        schema: {
          key: 'status',
          label: 'Status',
          type: 'select',
          options: [
            { label: 'Active', value: 'active' },
            { label: 'Inactive', value: 'inactive' },
          ],
        },
        modelValue: 'active',
        state: 'idle',
      },
    })

    // Should display the selected option label
    expect(wrapper.text()).toContain('Active')
  })

  it('displays checkbox value as Yes/No', async () => {
    const wrapperYes = await mountSuspended(DataFormField, {
      props: {
        schema: { key: 'active', label: 'Active', type: 'checkbox' },
        modelValue: true,
        state: 'idle',
      },
    })
    expect(wrapperYes.text()).toContain('Yes')

    const wrapperNo = await mountSuspended(DataFormField, {
      props: {
        schema: { key: 'active', label: 'Active', type: 'checkbox' },
        modelValue: false,
        state: 'idle',
      },
    })
    expect(wrapperNo.text()).toContain('No')
  })
})
