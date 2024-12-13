<template>
  <div>
    <p>User Logged In: {{ userStore.isLoggedIn }}</p>
    <p>User Data: {{ userStore.userData }}</p>

    <button @click="logout">Logout</button>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()


const logout = () => {
  userStore.logout()
}
</script>
