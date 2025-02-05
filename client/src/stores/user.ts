import { defineStore } from 'pinia'
import { useStorage, StorageSerializers } from '@vueuse/core'
import { computed } from 'vue'
import type { User } from '@/types/user'
import server from '@/utils/server'
import { isAxiosError } from 'axios'
import router from '@/router'
import { useMessageStore } from './message'

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
  const messageStore = useMessageStore()
  const login = async (body: { username: string; password: string }) => {
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
        messageStore.showMessage('Error', 'Login failed. Please try again.', 'error')
      } else {
        messageStore.showMessage('Error', 'An unexpected error occured. Please try again.', 'error')
      }
      return false
    }
  }

  const registerUser = async (body: {
    username: string
    email: string
    first_name: string
    last_name: string
    birthdate: string
    gender_identity: number
    indigenous_identity: number
    password: string
  }) => {
    try {
      // API call to register using axios server instance
      const response = await server.post('/register/', body)
      messageStore.showMessage('Success', 'Registration successful', 'success')
      return true
    } catch (error) {
      if (isAxiosError(error)) {
        messageStore.showMessage('Error', 'Registration failed.', 'error')
      } else {
        messageStore.showMessage('Error', 'An unexpected error occured. Please try again.', 'error')
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
