export function useApiFetch<T = any>(url: string, options: any = {}) {
  return useFetch<T>(url, {
    baseURL: '/db',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    ...options
  })
}

export async function apiGet<T = any>(url: string, params?: Record<string, any>, options?: any): Promise<T> {
  return $fetch<T>(url, {
    method: 'GET',
    baseURL: '/db',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    params,
    ...options
  })
}

export async function apiPost<T = any>(url: string, data?: any, options?: any): Promise<T> {
  return $fetch<T>(url, {
    method: 'POST',
    baseURL: '/db',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: data,
    ...options
  })
}

export async function apiPut<T = any>(url: string, data?: any, options?: any): Promise<T> {
  return $fetch<T>(url, {
    method: 'PUT',
    baseURL: '/db',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: data,
    ...options
  })
}

export async function apiDelete<T = any>(url: string, options?: any): Promise<T> {
  return $fetch<T>(url, {
    method: 'DELETE',
    baseURL: '/db',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    ...options
  })
}
