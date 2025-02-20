import axios, { AxiosError } from 'axios'
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
  async (error: AxiosError & { config: { token_refreshed?: boolean } }) => {
    const userStore = useUserStore()
    if (error.response?.status === 401 && userStore.refreshToken && !error.config.token_refreshed) {
      try {
        const response = await axios.post(
          `${import.meta.env.VITE_BACKEND_URL}/api/token/refresh/`,
          {
            refresh: userStore.refreshToken,
          },
        )
        // Update access token in store
        if (response.data.access) {
          userStore.accessToken = response.data.access
          // Mark the token as already refreshed
          // The importance of this is that it avoids an infinite loop of refresh attemps if
          // the refresh endpoint is broken yet keeps returning a 401 status code
          error.config.token_refreshed = true
          return server(error.config)
        }
        // if the response doesn't contain an access token for some reason, then logout
        userStore.logout()
      } catch {
        // This will run if the call to the token endpoint is unsucessful (meaning the refresh token is invalid, so a login is required)
        userStore.logout()
      }
    }

    return Promise.reject(error)
  },
)

export default server
