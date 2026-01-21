import { nextTick } from 'vue'
import { describe, it, expect } from 'vitest'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import DataTable from '../../app/components/DataTable.vue'

describe('DataTable (Nuxt Integration)', () => {
  it('renders in Nuxt environment', async () => {
    const data = [
      { id: '1', name: 'Item 1', status: 'active' },
      { id: '2', name: 'Item 2', status: 'inactive' }
    ]

    const columns = [
      { accessorKey: 'name', header: 'Name' },
      { accessorKey: 'status', header: 'Status' }
    ]

    const component = await mountSuspended(DataTable, {
      props: { data, columns, cardFields: ['name'] }
    })

    expect(component.html()).toContain('Item 1')
    expect(component.html()).toContain('Item 2')
  })

  it('switches between table and grid view', async () => {
    const data = [{ id: '1', name: 'Item' }]
    const columns = [{ accessorKey: 'name', header: 'Name' }]

    const component = await mountSuspended(DataTable, {
      props: { data, columns, viewMode: 'table', cardFields: ['name'] } as any
    })

    const tableElement = component.find('[class*="table"]')
    expect(tableElement.exists()).toBe(true)

    // Update viewMode via props
    await component.setProps({ viewMode: 'grid' })
    await nextTick()

    // Check if grid view is rendered
    // Note: Nuxt UI components might render different structures, but .grid should exist in our v-else
    const html = component.html()
    expect(html).toContain('grid')
  })

  it('displays empty state', async () => {
    const component = await mountSuspended(DataTable, {
      props: { data: [], columns: [], cardFields: [] } as any
    })

    expect(component.text()).toContain('No items found.')
  })

})
