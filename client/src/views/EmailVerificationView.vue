<script setup lang="ts">
import { onMounted } from 'vue'
import axios from 'axios'
import { useMessageStore } from '@/stores/message'
import { useRouter } from 'vue-router'

// use defineProps to receive the token from the router
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
    await axios.post('/api/verify-email', {
      token: props.token,
    })
    messageStore.showMessage('Success', 'Email verified successfully', 'success')
  } catch (error) {
    console.error('Email verification failed:', error)
    messageStore.showMessage('Error', 'Invalid verification link.', 'error')
  }
})
</script>

<template>
  <div class="d-flex justify-center align-center full-screen flex-column">
    <h2>Verifying your email.</h2>
    <a @click="goToHomePage" class="mt-3 homepage-link">Go to Homepage</a>
  </div>
</template>

<style scoped>
.full-screen {
  height: 100vh;
}

.homepage-link {
  text-decoration: none;
  color: #0056b3;
}

.homepage-link:hover {
  text-decoration: underline;
  color: #0056b3;
}
</style>
