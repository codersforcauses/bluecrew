<script setup lang="ts">
import ChallengeCard from '@/components/ChallengeCard.vue'
import { ref } from 'vue'

const dialog = ref(false)

const handleClose = () => {
  dialog.value = false
}

const handleTaskCompleted = () => {
  setTimeout(() => {
    dialog.value = false
  }, 2000)
}

const handleIconClick = () => {
  dialog.value = true
}
</script>

<template>
  <img
    src="../assets/BrainIcon.svg"
    alt="Brain icon"
    @click="handleIconClick"
    class="cursor-pointer"
  />

  <v-dialog v-model="dialog" width="500">
    <ChallengeCard @close="handleClose" @task-completed="handleTaskCompleted" />
  </v-dialog>
</template>
