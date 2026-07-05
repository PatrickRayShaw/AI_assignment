import api from './index'

export const semanticSearch = (query) => api.post('/search/semantic', { query })
export const getSearchHistory = () => api.get('/search/history')
