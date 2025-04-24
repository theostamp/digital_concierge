// 📁 lib/axios-auth.ts

import axios from 'axios'
import Cookies from 'js-cookie'

const axiosAuth = axios.create({ baseURL: '/api' })

axiosAuth.interceptors.request.use((config) => {
  const token = Cookies.get('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

axiosAuth.interceptors.response.use(
  res => res,
  async error => {
    const originalRequest = error.config
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refreshToken = Cookies.get('refresh_token')
      if (refreshToken) {
        try {
          interface RefreshResponse {
            access: string;
          }
          const response = await axios.post<RefreshResponse>('/api/token/refresh/', { refresh: refreshToken })
          const newAccess = response.data.access
          Cookies.set('access_token', newAccess, { path: '/' })
          axios.defaults.headers.common['Authorization'] = `Bearer ${newAccess}`
          originalRequest.headers['Authorization'] = `Bearer ${newAccess}`
          return axios(originalRequest)
        } catch {
          Cookies.remove('access_token')
          Cookies.remove('refresh_token')
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(new Error(error.message ?? 'An unknown error occurred'))
  }
)

export default axiosAuth
