<script setup lang="ts">
import { RouterView } from 'vue-router'
import RegisterModal from './components/RegisterModal.vue'
</script>

<template>
  <div class="pa-4 text-center">
    <RegisterModal />
    <RouterView />
  </div>
</template>

<style scoped></style>