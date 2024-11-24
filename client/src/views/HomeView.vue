<script setup lang="ts">
import { ref } from 'vue'
import server from '@/utils/server'

const isLoading = ref(false)
const healthcheckMessage = ref('')

const handlePing = async () => {
  isLoading.value = true
  healthcheckMessage.value = '' // Clear previous messages

  try {
    const response = await server.get('/healthcheck/ping/')
    healthcheckMessage.value = response.data
  } catch {
    healthcheckMessage.value = 'Failed to ping server'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div id="healthcheck">
    <h1>Healthcheck</h1>
    <button id="ping" @click="handlePing" :disabled="isLoading">
      {{ isLoading ? 'Loading' : 'Ping' }}
    </button>
    <p>
      Response from server: <span>{{ healthcheckMessage }}</span>
    </p>
  </div>
</template>

<style scoped>
#healthcheck {
  display: flex;
  flex-direction: column;
  place-items: center;
  height: 80vh;
}

#ping {
  background-color: var(--color-text);
  color: var(--color-background);
  border: none;
  border-radius: 2px;
  padding: 8px 16px;
  margin: 8px;
}

#ping:hover {
  filter: brightness(80%);
}
</style>
