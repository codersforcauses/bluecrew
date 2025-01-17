import { defineStore } from 'pinia'
import { useStorage } from '@vueuse/core'
import { computed } from 'vue'
import type { User } from '@/types/user'
import { useRouter } from 'vue-router'

export const useUserStore = defineStore('user', () => {
  const router = useRouter()
  const userData = useStorage<User | null>('userData', null)
  const accessToken = useStorage<string | null>('accessToken', null)
  const refreshToken = useStorage<string | null>('refreshToken', null)

  const isLoggedIn = computed(() => userData.value !== null)

  //Logout Status
  const logout = () => {
    userData.value = null
    accessToken.value = null
    refreshToken.value = null
    router.push({ name: 'landing' })
  }

  return {
    userData,
    isLoggedIn,
    accessToken,
    refreshToken,
    logout,
  }
})
