<script setup lang="ts">
import { useModalStore } from '@/stores/modal'
import { RouterView } from 'vue-router'
import LoginModal from './components/LoginModal.vue'
import BluecrewFooter from '@/components/BluecrewFooter.vue'
import RegisterModal from '@/components/RegisterModal.vue'

const modalStore = useModalStore()
</script>

<template>
  <RouterView />
  <BluecrewFooter />
  <RegisterModal v-if="modalStore.currentModal === 'register'" @close="modalStore.closeModal" />
  <LoginModal v-if="modalStore.currentModal === 'login'" @close="modalStore.closeModal" />
</template>

<style scoped></style>
