import axios from 'axios'
import { useUserStore } from '@/stores/user'

const server = axios.create({
  baseURL: `${import.meta.env.VITE_BACKEND_URL}/api`,
  timeout: 8000,
})

// Add request interceptor: add access token to request headers
server.interceptors.request.use(
  (config) => {
    const userStore = useUserStore()
    if (userStore.accessToken) {
      config.headers.Authorization = `Bearer ${userStore.accessToken}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// Add response interceptor: handle 401 error and refresh token
server.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const userStore = useUserStore()

    // Handle 401 error
    if (error.response?.status === 401 && userStore.refreshToken) {
      try {
        // Store old token
        const oldAccessToken = userStore.accessToken

        // Try to refresh token using HTTP request
        const response = await axios.post(
          `${import.meta.env.VITE_BACKEND_URL}/api/token/refresh/`,
          {
            refresh: userStore.refreshToken,
          },
        )
        // Update access token in store
        if (response.data.access) {
          userStore.accessToken = response.data.access
          // If new token obtained, retry original request
          if (userStore.accessToken !== oldAccessToken) {
            const config = error.config
            config.headers.Authorization = `Bearer ${userStore.accessToken}`
            return server(config)
          }
        }
      } catch {
        // Refresh token expired, need to login again
        userStore.logout()
      }
    }

    return Promise.reject(error)
  },
)

export default server
