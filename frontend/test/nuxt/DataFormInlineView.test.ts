import { describe, expect, it, vi, beforeEach, afterEach } from 'vitest'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import DataFormInlineView from '~/components/DataFormInlineView.vue'
import type { FieldSchema } from '~/shared/types/ui'

const mockFetch = vi.fn()
vi.stubGlobal('$fetch', mockFetch)

describe('DataFormInlineView', () => {
  const basicSchema: FieldSchema[] = [
    { key: 'quantity', label: 'Quantity', type: 'number', required: true },
    { key: 'designators', label: 'Designators', type: 'text' },
  ]

  const basicItems = [
    { id: '1', quantity: 10, designators: 'R1, R2' },
    { id: '2', quantity: 5, designators: 'C1' },
  ]

  beforeEach(() => {
    mockFetch.mockReset()
    mockFetch.mockResolvedValue({ success: true })
  })

  afterEach(() => {
    vi.clearAllMocks()
  })

  it('renders title and add button', async () => {
    const wrapper = await mountSuspended(DataFormInlineView, {
      props: {
        items: basicItems,
        itemSchema: basicSchema,
        baseEndpoint: '/projects/123/bom',
        title: 'BOM Items',
      },
    })

    expect(wrapper.text()).toContain('BOM Items')
    expect(wrapper.text()).toContain('Add Item')
  })

  it('renders items in table', async () => {
    const wrapper = await mountSuspended(DataFormInlineView, {
      props: {
        items: basicItems,
        itemSchema: basicSchema,
        baseEndpoint: '/projects/123/bom',
        title: 'BOM Items',
      },
    })

    expect(wrapper.text()).toContain('10')
    expect(wrapper.text()).toContain('R1, R2')
    expect(wrapper.text()).toContain('5')
    expect(wrapper.text()).toContain('C1')
  })

  it('shows empty state when no items', async () => {
    const wrapper = await mountSuspended(DataFormInlineView, {
      props: {
        items: [],
        itemSchema: basicSchema,
        baseEndpoint: '/projects/123/bom',
        title: 'BOM Items',
        emptyStateMessage: 'No BOM items',
      },
    })

    expect(wrapper.text()).toContain('No BOM items')
  })

  it('shows custom empty state message', async () => {
    const wrapper = await mountSuspended(DataFormInlineView, {
      props: {
        items: [],
        itemSchema: basicSchema,
        baseEndpoint: '/projects/123/bom',
        title: 'BOM Items',
        emptyStateMessage: 'Custom empty message',
      },
    })

    expect(wrapper.text()).toContain('Custom empty message')
  })

  it('hides add button when canEdit is false', async () => {
    const wrapper = await mountSuspended(DataFormInlineView, {
      props: {
        items: basicItems,
        itemSchema: basicSchema,
        baseEndpoint: '/projects/123/bom',
        title: 'BOM Items',
        canEdit: false,
      },
    })

    expect(wrapper.text()).not.toContain('Add Item')
  })

  it('hides delete button when canDelete is false', async () => {
    const wrapper = await mountSuspended(DataFormInlineView, {
      props: {
        items: basicItems,
        itemSchema: basicSchema,
        baseEndpoint: '/projects/123/bom',
        title: 'BOM Items',
        canDelete: false,
      },
    })

    expect(wrapper.findAll('button').filter(b => b.text().includes('trash')).length).toBe(0)
  })

  it('displays custom display columns', async () => {
    const wrapper = await mountSuspended(DataFormInlineView, {
      props: {
        items: basicItems,
        itemSchema: basicSchema,
        displayColumns: [{ key: 'status', label: 'Status' }],
        baseEndpoint: '/projects/123/bom',
        title: 'BOM Items',
      },
    })

    expect(wrapper.text()).toContain('Status')
  })

  it('calls DELETE endpoint when delete is clicked', async () => {
    const wrapper = await mountSuspended(DataFormInlineView, {
      props: {
        items: basicItems,
        itemSchema: basicSchema,
        baseEndpoint: '/projects/123/bom',
        title: 'BOM Items',
      },
    })

    const trashButton = wrapper.find('button[aria-label="trash"]')
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    
    await trashButton.trigger('click')
    
    expect(mockFetch).toHaveBeenCalledWith('/db/projects/123/bom/1', { method: 'DELETE' })
  })

  it('does not call DELETE when confirmation is cancelled', async () => {
    const wrapper = await mountSuspended(DataFormInlineView, {
      props: {
        items: basicItems,
        itemSchema: basicSchema,
        baseEndpoint: '/projects/123/bom',
        title: 'BOM Items',
      },
    })

    const trashButton = wrapper.find('button[aria-label="trash"]')
    vi.spyOn(window, 'confirm').mockReturnValue(false)
    
    await trashButton.trigger('click')
    
    expect(mockFetch).not.toHaveBeenCalled()
  })

  it('shows add form when add button is clicked', async () => {
    const wrapper = await mountSuspended(DataFormInlineView, {
      props: {
        items: basicItems,
        itemSchema: basicSchema,
        baseEndpoint: '/projects/123/bom',
        title: 'BOM Items',
      },
    })

    await wrapper.find('button:contains("Add Item")').trigger('click')
    
    expect(wrapper.text()).toContain('Add New Item')
    expect(wrapper.text()).toContain('Quantity')
    expect(wrapper.text()).toContain('Designators')
  })

  it('calls POST endpoint when adding item', async () => {
    const wrapper = await mountSuspended(DataFormInlineView, {
      props: {
        items: basicItems,
        itemSchema: basicSchema,
        baseEndpoint: '/projects/123/bom',
        title: 'BOM Items',
      },
    })

    await wrapper.find('button:contains("Add Item")').trigger('click')
    
    const quantityInput = wrapper.find('input[type="number"]')
    await quantityInput.setValue(25)
    
    const designatorsInput = wrapper.find('input[placeholder="Search..."]')
    await designatorsInput.setValue('R5-R10')
    
    mockFetch.mockResolvedValue({ id: '3', quantity: 25, designators: 'R5-R10' })
    
    await wrapper.find('button:contains("Add Item")').trigger('click')
    
    expect(mockFetch).toHaveBeenCalledWith('/db/projects/123/bom', {
      method: 'POST',
      body: expect.objectContaining({ quantity: 25, designators: 'R5-R10' })
    })
  })

  it('shows loading state', async () => {
    const wrapper = await mountSuspended(DataFormInlineView, {
      props: {
        items: [],
        itemSchema: basicSchema,
        baseEndpoint: '/projects/123/bom',
        title: 'BOM Items',
        loading: true,
      },
    })

    expect(wrapper.find('.animate-spin').exists()).toBe(true)
  })
})
