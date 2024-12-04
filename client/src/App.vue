<script setup lang="ts">
import { RouterView } from 'vue-router'
import RegisterModal from './components/RegisterModal.vue'
import { ref } from 'vue'

const isOpen = ref(false)
</script>

<template>
  <RouterView />
  <button @click="isOpen = true">Register</button>
  <RegisterModal :open="'isOpen'" @close="isOpen = !isOpen"></RegisterModal>
</template>

<style scoped>
button {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.16);
}
</style>
