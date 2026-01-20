import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import DataTable from '../../app/components/DataTable.vue'

describe('DataTable', () => {
  it('renders correctly with data and columns', () => {
    const data = [
      { id: '1', name: 'Item 1', status: 'active' },
      { id: '2', name: 'Item 2', status: 'inactive' }
    ]

    const columns = [
      { accessorKey: 'name', header: 'Name' },
      { accessorKey: 'status', header: 'Status' }
    ]

    const wrapper = mount(DataTable, {
      props: { data, columns }
    })

    expect(wrapper.exists()).toBe(true)
  })

  it('displays empty state when no data', () => {
    const wrapper = mount(DataTable, {
      props: { data: [], columns: [] }
    })

    expect(wrapper.text('No items found.')).toBeTruthy()
  })

  it('displays loading state', () => {
    const wrapper = mount(DataTable, {
      props: { data: [], columns: [], loading: true }
    })

    expect(wrapper.find('[class*="skeleton"]')).toBeTruthy()
  })

  it('supports view mode toggle', () => {
    const wrapper = mount(DataTable, {
      props: {
        data: [{ id: '1', name: 'Item' }],
        columns: [{ accessorKey: 'name', header: 'Name' }],
        viewMode: 'grid'
      }
    })

    expect(wrapper.find('[class*="grid"]')).toBeTruthy()
  })

  it('emits row-click event', async () => {
    const data = [{ id: '1', name: 'Item' }]
    const onRowClick = vi.fn()

    const wrapper = mount(DataTable, {
      props: {
        data,
        columns: [{ accessorKey: 'name', header: 'Name' }],
        clickableColumn: 'name',
        onRowClick: onRowClick
      }
    })

    await wrapper.find('[class*="font-medium"]').trigger('click')
    expect(onRowClick).toHaveBeenCalled()
  })

  it('applies default sorting', () => {
    const data = [
      { id: '2', name: 'Item 2', status: 'inactive' },
      { id: '1', name: 'Item 1', status: 'active' }
    ]

    const wrapper = mount(DataTable, {
      props: {
        data,
        columns: [{ accessorKey: 'name', header: 'Name' }],
        defaultSort: { id: 'name', desc: false }
      }
    })

    const items = wrapper.findAll('[class*="font-medium"]')
    expect(items[0].text()).toBe('Item 1')
    expect(items[1].text()).toBe('Item 2')
  })
})
