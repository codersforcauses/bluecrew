<script setup lang="ts">
import { ref } from 'vue'
import { useModalStore } from '@/stores/modal'
import server from '@/utils/server'
import RegisterModal from '@/components/RegisterModal.vue'

const modalStore = useModalStore()

function openRegisterButton() {
  modalStore.openRegister()
}

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
  <v-btn
    id="register-button"
    class="bg-primaryBlue text-creamyWhite d-flex justify-center align-center"
    @click="openRegisterButton"
  >
    Registration
  </v-btn>

  <RegisterModal v-if="modalStore.currentModal === 'register'" @close="modalStore.closeModal" />

  <div id="healthcheck">
    <h1>Healthcheck <v-icon icon="mdi-heart-pulse" /></h1>
    <v-btn id="ping" @click="handlePing" :loading="isLoading">
      {{ isLoading ? 'Loading' : 'Ping' }}
    </v-btn>
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
