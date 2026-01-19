export const useApiFetch = (url: string, options: any = {}) => {
    const config = useRuntimeConfig()

    // Base fetch options
    const defaults = {
        baseURL: '/db',
        // In a real app, we'd add auth headers here
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        ...options
    }

    return useFetch(url, defaults)
}
