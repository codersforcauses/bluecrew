<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useModalStore } from '@/stores/modal'
import BluecrewFooter from '@/components/BluecrewFooter.vue'
import RegisterModal from './components/RegisterModal.vue'

const modalStore = useModalStore()

function openRegisterButton() {
  modalStore.openRegister()
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

  <RouterView />
  <BluecrewFooter />
</template>

<style scoped></style>
