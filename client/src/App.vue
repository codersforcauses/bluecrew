<script setup lang="ts">
import { RouterView } from 'vue-router'
import BluecrewFooter from '@/components/BluecrewFooter.vue'
import RegisterModal from './components/RegisterModal.vue'
</script>

<template>
  <RegisterModal />
  <RouterView />
  <BluecrewFooter />
</template>

<style scoped></style>
