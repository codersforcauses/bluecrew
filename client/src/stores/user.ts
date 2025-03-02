import { defineStore } from 'pinia'
import { useStorage, StorageSerializers } from '@vueuse/core'
import { computed } from 'vue'
import type { BackendUser, BackendUserErrors, ResetPasswordErrors, User } from '@/types/user'
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

  const registerUser = async (body: BackendUser): Promise<boolean | BackendUserErrors> => {
    try {
      // API call to register using axios server instance
      await server.post('/register/', body)
      return true
    } catch (error) {
      if (isAxiosError(error)) {
        if (error.response?.status === 400) {
          return error.response.data as BackendUserErrors
        }
      }
      return false
    }
  }

  const requestEmailVerification = async (email: string): Promise<boolean | string> => {
    try {
      await server.post('/email-validation/', { email })
      return true
    } catch (error) {
      if (isAxiosError(error)) {
        if (error.response?.status === 400) {
          return error.response.data as string
        }
      }
      return false
    }
  }

  const verifyEmail = async (uid: string, token: string): Promise<boolean> => {
    try {
      await server.post('/activate/', {
        token,
        uid64: uid,
      })
      return true
    } catch {
      return false
    }
  }

  const requestPasswordReset = async (email: string): Promise<boolean | string> => {
    try {
      await server.post('/request-reset/', { email })
      return true
    } catch (error) {
      if (isAxiosError(error)) {
        if (error.response?.status === 400) {
          return error.response.data as string
        }
      }
      return false
    }
  }

  const resetPassword = async (
    password: string,
    uid: string,
    token: string,
  ): Promise<boolean | ResetPasswordErrors> => {
    try {
      await server.post('/reset-password/', {
        password,
        token,
        uid64: uid,
      })
      return true
    } catch (error) {
      if (isAxiosError(error)) {
        if (error.response?.status === 404) {
          return 'invalid link'
        } else if (error.response?.status === 400) {
          if (error.response?.data === 'User ID invalid.') {
            return 'invalid link'
          }
          return error.response.data as [string, ...string[]]
        }
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
    requestEmailVerification,
    requestPasswordReset,
    verifyEmail,
    resetPassword,
  }
})
