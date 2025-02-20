<script setup lang="ts">
import { onMounted } from 'vue'
import axios from 'axios'
import { useMessageStore } from '@/stores/message'
import { useRouter } from 'vue-router'

const props = defineProps<{ token?: string }>()
const messageStore = useMessageStore()
const router = useRouter()

const goToHomePage = () => {
  router.push({ path: '/' })
}

onMounted(async () => {
  if (!props.token) {
    messageStore.showMessage('Error', 'Invalid verification link.', 'error')
    return
  }

  try {
    await axios.post('/api/verify-email/', {
      token: props.token,
    })
    messageStore.showMessage('Success', 'Email verified successfully', 'success')
  } catch {
    messageStore.showMessage('Error', 'Invalid verification link.', 'error')
  }
})
</script>

<template>
  <div class="d-flex justify-center align-center full-screen flex-column">
    <h2>Verifying your email.</h2>
    <v-btn class="mt-3" color="primaryBlue" @click="goToHomePage"> Go to Homepage </v-btn>
  </div>
</template>

<style scoped>
.full-screen {
  height: 100vh;
}
</style>
