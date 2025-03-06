<script setup lang="ts">
import { useModalStore } from '@/stores/modal'
import { useUserStore } from '@/stores/user'
import { RouterView } from 'vue-router'
import { useDisplay } from 'vuetify'
import LoginModal from './components/LoginModal.vue'
import BluecrewFooter from '@/components/BluecrewFooter.vue'
import RegisterModal from '@/components/RegisterModal.vue'
import NavBarWrapper from './components/NavBarWrapper.vue'
import GenericMessage from '@/components/GenericMessage.vue'

const { xs } = useDisplay()
const modalStore = useModalStore()
const userStore = useUserStore()
</script>

<template>
  <v-app>
    <NavBarWrapper />
    <v-main :class="{ 'mt-14': !xs }">
      <RouterView :key="userStore.isLoggedIn ? 1 : 0" />
      <GenericMessage />
    </v-main>
    <BluecrewFooter />
  </v-app>
  <RegisterModal v-if="modalStore.currentModal === 'register'" @close="modalStore.closeModal" />
  <LoginModal v-if="modalStore.currentModal === 'login'" @close="modalStore.closeModal" />
</template>
