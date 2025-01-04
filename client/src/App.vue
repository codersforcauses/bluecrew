<script setup lang="ts">
import { RouterView } from 'vue-router'
import LoginModal from './components/LoginModal.vue'
import { useModalStore } from '@/stores/modal';

const modalStore = useModalStore()
</script>

<template>
  <RouterView />
  <LoginModal v-if="modalStore.currentModal === 'login'" @close="modalStore.closeModal" />
</template>

<style></style>
