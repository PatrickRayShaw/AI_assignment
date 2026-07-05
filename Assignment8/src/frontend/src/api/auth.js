import api from './index'

export const loginAPI = (data) => api.post('/auth/login', data)
export const registerAPI = (data) => api.post('/auth/register', data)
export const getUserInfoAPI = () => api.get('/auth/me')
