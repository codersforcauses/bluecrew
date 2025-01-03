<script setup lang="ts">
import { RouterView } from 'vue-router'
import BluecrewFooter from '@/components/BluecrewFooter.vue'
import RegisterModal from '@/components/RegisterModal.vue'
</script>

<template>
  <RouterView />
  <BluecrewFooter />
  <RegisterModal />
</template>

<style scoped></style>
