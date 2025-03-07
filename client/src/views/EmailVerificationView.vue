<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useMessageStore } from '@/stores/message'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const props = defineProps<{ token?: string; uid?: string }>()
const messageStore = useMessageStore()
const userStore = useUserStore()
const router = useRouter()
const text = ref('Verifying your email...')

const goToHomePage = () => {
  router.push({ path: '/' })
}

onMounted(async () => {
  if (!props.token || !props.uid) {
    messageStore.showMessage('Error', 'Invalid verification link.', 'error')
    return
  }

  const verificationResult = await userStore.verifyEmail(props.uid, props.token)
  if (verificationResult) {
    text.value = 'Email Verified!'
    messageStore.showMessage('Success', 'Email verified successfully', 'success')
  } else {
    text.value = 'Invalid verification link.'
    messageStore.showMessage('Error', 'Invalid verification link.', 'error')
  }
})
</script>

<template>
  <div class="d-flex justify-center align-center h-100 flex-column">
    <h2>{{ text }}</h2>
    <v-btn class="mt-3" color="primaryBlue" @click="goToHomePage"> Go to Homepage </v-btn>
  </div>
</template>

<style scoped>
.full-screen {
  height: 100vh;
}
</style>
