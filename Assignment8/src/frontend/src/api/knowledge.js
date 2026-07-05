import api from './index'

export const getNewsList = (params) => api.get('/knowledge/list', { params })
export const getNewsDetail = (id) => api.get(`/knowledge/${id}`)
export const createNews = (data) => api.post('/knowledge/create', data)
export const updateNews = (id, data) => api.put(`/knowledge/${id}`, data)
export const deleteNews = (id) => api.delete(`/knowledge/${id}`)
export const batchDeleteNews = (ids) => api.post('/knowledge/batch-delete', { ids })
export const getTags = () => api.get('/knowledge/tags')
