import { defineStore } from 'pinia'
import { useStorage } from '@vueuse/core'
import { computed } from 'vue'

// User interface (include userName, name and email)
interface User {
  userName: string
  name: string
  email: string
}

export const useUserStore = defineStore('user', () => {
  const userData = useStorage<User | null>('userData', null)
  const accessToken = useStorage<string | null>('accessToken', null)
  const refreshToken = useStorage<string | null>('refreshToken', null)

  const isLoggedIn = computed(() => !!userData.value)

  // Login Status
  const login = (user: User, tokens: { accessToken: string; refreshToken: string }) => {
    userData.value = user
    accessToken.value = tokens.accessToken
    refreshToken.value = tokens.refreshToken
  }

  //Logout Status
  const logout = () => {
    userData.value = null
    accessToken.value = null
    refreshToken.value = null
  }

  return {
    userData,
    isLoggedIn,
    accessToken,
    refreshToken,
    login,
    logout,
  }
})
