import { describe, it, expect } from 'vitest'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import DataTable from '../app/components/DataTable.vue'

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
      props: { data, columns }
    })

    expect(component.html()).toContain('Item 1')
    expect(component.html()).toContain('Item 2')
  })

  it('switches between table and grid view', async () => {
    const data = [{ id: '1', name: 'Item' }]
    const columns = [{ accessorKey: 'name', header: 'Name' }]

    const component = await mountSuspended(DataTable, {
      props: { data, columns, viewMode: 'table' }
    })

    const tableElement = component.find('[class*="table"]')
    expect(tableElement).toBeTruthy()

    await component.setData({ viewMode: 'grid' })
    await nextTick()

    const gridElement = component.find('[class*="grid"]')
    expect(gridElement).toBeTruthy()
    expect(tableElement).toBeFalsy()
  })

  it('displays empty state', async () => {
    const component = await mountSuspended(DataTable, {
      props: { data: [], columns: [] }
    })

    expect(component.text('No items found.')).toBeTruthy()
  })

})
