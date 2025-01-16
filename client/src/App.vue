<script setup lang="ts">
import { useModalStore } from '@/stores/modal'
import { RouterView } from 'vue-router'
import LoginModal from './components/LoginModal.vue'
import BluecrewFooter from '@/components/BluecrewFooter.vue'
import RegisterModal from '@/components/RegisterModal.vue'
import NavBarWrapper from './components/NavBarWrapper.vue'
import ChallengeCard from './components/ChallengeCard.vue'

const modalStore = useModalStore()
</script>

<template>
  <v-app>
    <NavBarWrapper />
    <v-main class="main-content">
      <RouterView />
    </v-main>
    <BluecrewFooter />
  </v-app>
  <RegisterModal v-if="modalStore.currentModal === 'register'" @close="modalStore.closeModal" />
  <LoginModal v-if="modalStore.currentModal === 'login'" @close="modalStore.closeModal" />
</template>

<style scoped>
.main-content {
  margin-top: 56px;
}
</style>
