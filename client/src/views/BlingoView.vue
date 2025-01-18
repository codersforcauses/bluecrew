<script setup lang="ts">
import ChallengeCard from '@/components/ChallengeCard.vue'
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useModalStore } from '@/stores/modal'
const dialog = ref(false)
const modalStore = useModalStore()
const handleClose = () => {
  dialog.value = false
}

const userStore = useUserStore()
const handleIconClick = () => {
  if (userStore.isLoggedIn) {
    dialog.value = true
  } else {
    // dialog.value = true
    modalStore.openLogin()
  }
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
    <ChallengeCard @close="handleClose" />
  </v-dialog>
</template>
