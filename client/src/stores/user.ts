import { defineStore } from 'pinia'
import { useStorage, StorageSerializers } from '@vueuse/core'
import { computed } from 'vue'
import type { BackendUser, User } from '@/types/user'
import server from '@/utils/server'
import { isAxiosError } from 'axios'
import router from '@/router'

export const useUserStore = defineStore('user', () => {
  const userData = useStorage<User | null>('userData', null, undefined, {
    serializer: StorageSerializers.object,
  })
  const accessToken = useStorage<string | null>('accessToken', null)
  const refreshToken = useStorage<string | null>('refreshToken', null)

  const isLoggedIn = computed(() => userData.value !== null)
  const normalUserLoggedIn = computed(() => userData.value !== null && !userData.value.isSuperuser)
  const superUserLoggedIn = computed(() => userData.value !== null && userData.value.isSuperuser)

  //Logout Status
  const logout = () => {
    userData.value = null
    accessToken.value = null
    refreshToken.value = null
    if (router.currentRoute.value.meta.requiresAuth === true) {
      router.push('/')
    }
  }

  const login = async (body: {
    username: string
    password: string
  }): Promise<boolean | 'invalid'> => {
    try {
      const tokenResponse = await server.post('/token/', body)
      const { access, refresh } = tokenResponse.data
      accessToken.value = access
      refreshToken.value = refresh

      const userResponse = await server.get('/user/me/')
      userData.value = userResponse.data
      return true
    } catch (error) {
      if (isAxiosError(error)) {
        if (error.response?.status === 401) {
          return 'invalid'
        }
      }
      return false
    }
  }

  const registerUser = async (body: BackendUser) => {
    try {
      // API call to register using axios server instance
      const response = await server.post('/register/', body)
      console.log('Registration successful:', response.data)
      return true
    } catch (error) {
      if (isAxiosError(error)) {
      }
      return false
    }
  }

  return {
    userData,
    isLoggedIn,
    normalUserLoggedIn,
    superUserLoggedIn,
    accessToken,
    refreshToken,
    logout,
    login,
    registerUser,
  }
})
