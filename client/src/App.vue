<script setup lang="ts">
import { useModalStore } from '@/stores/modal'
import { RouterView } from 'vue-router'
import BluecrewFooter from '@/components/BluecrewFooter.vue'
import RegisterModal from '@/components/RegisterModal.vue'

const modalStore = useModalStore()
</script>

<template>
  <RouterView />
  <BluecrewFooter />
  <RegisterModal />
  <RegisterModal v-if="modalStore.currentModal === 'register'" @close="modalStore.closeModal" />
</template>

<style scoped></style>
