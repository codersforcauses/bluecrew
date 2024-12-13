<template>
  <div>
    <p>User Logged In: {{ userStore.isLoggedIn }}</p>
    <p>User Data: {{ userStore.userData }}</p>
    <button @click="login">Login</button>
    <button @click="logout">Logout</button>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const login = () => {
  const user = { userName: 'testUser', name: 'Test User', email: 'test@example.com' }
  const tokens = { accessToken: 'accessToken123', refreshToken: 'refreshToken123' }
  userStore.login(user, tokens)
}

const logout = () => {
  userStore.logout()
}
</script>
