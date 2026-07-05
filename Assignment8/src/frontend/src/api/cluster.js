import api from './index'

export const analyzeCluster = () => api.post('/cluster/analyze')
export const getClusterReport = () => api.get('/cluster/report')
