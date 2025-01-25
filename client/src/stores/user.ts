import { defineStore } from 'pinia'
import { useStorage } from '@vueuse/core'
import { computed, ref } from 'vue'
import type { User } from '@/types/user'
import server from '@/utils/server'
import { isAxiosError } from 'axios'
import router from '@/router'

export const useUserStore = defineStore('user', () => {
  const userData = useStorage<User | null>('userData', null)
  const accessToken = useStorage<string | null>('accessToken', null)
  const refreshToken = useStorage<string | null>('refreshToken', null)
  const forceReload = ref<number>(0)

  const isLoggedIn = computed(() => userData.value !== null)

  //Logout Status
  const logout = () => {
    userData.value = null
    accessToken.value = null
    refreshToken.value = null
    if (router.currentRoute.value.meta.requiresAuth === true) {
      router.push('/')
    }
  }

  const login = async (body: { username: string; password: string }) => {
    try {
      const tokenResponse = await server.post('/token/', body)
      const { access, refresh } = tokenResponse.data
      accessToken.value = access
      refreshToken.value = refresh

      const userResponse = await server.get('/user/me/')
      userData.value = userResponse.data
      forceReload.value += 1
      return true
    } catch (error) {
      if (isAxiosError(error)) {
        console.error('Login failed:', error.response?.data || error)
        alert(`Error: ${error.response?.data?.message || 'Login failed.'}`)
      } else {
        console.error('Unexpected error:', error)
        alert('An unexpected error occured. Please try again.')
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
    gender_identity: string
    indigenous_identity: string
    password: string
  }) => {
    try {
      // API call to register using axios server instance
      const response = await server.post('/register/', body)

      console.log('Registration successful:', response.data)
      alert('Registration successful!')
      return true
    } catch (error) {
      if (isAxiosError(error)) {
        console.error('Registration failed:', error.response?.data || error)
        alert(`Error: ${error.response?.data?.message || 'Registration failed.'}`)
      } else {
        console.error('Unexpected error:', error)
        alert('An unexpected error occured. Please try again.')
      }
      return false
    }
  }

  return {
    userData,
    isLoggedIn,
    accessToken,
    refreshToken,
    forceReload,
    logout,
    login,
    registerUser,
  }
})
