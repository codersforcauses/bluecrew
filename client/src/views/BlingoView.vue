<script setup lang="ts">
import ChallengeCard from '@/components/ChallengeCard.vue'
import { ref } from 'vue'

const showChallenge = ref(true)

const handleClose = () => {
  showChallenge.value = false
}

const handleTaskCompleted = () => {
  // Show completed state for 2 seconds then close
  setTimeout(() => {
    showChallenge.value = false
  }, 2000)
}
</script>

<template>
  <ChallengeCard v-if="showChallenge" @close="handleClose" @task-completed="handleTaskCompleted" />
</template>
