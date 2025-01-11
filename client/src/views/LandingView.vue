<script setup lang="ts">
import { useModalStore } from '@/stores/modal'
import { useDisplay } from 'vuetify'

const { xs } = useDisplay()
const modalStore = useModalStore()

const openRegisterModal = () => {
  modalStore.openRegister()
}

const openLoginModal = () => {
  modalStore.openLogin()
}
</script>

<template>
  <v-container fluid class="fill-height pa-0 flex-column">
    <v-row v-if="!xs" class="header">
      <img src="/beach-header.jpg" alt="Ocean Beach" class="header-image" />
    </v-row>
    <v-row class="flex-grow-1 w-100" align="center">
      <v-col cols="12" sm="6" align-self="center">
        <v-row align="center">
          <v-col align="right"><img src="/bc-logo.png" alt="Blue Crew Logo" class="logo" /> </v-col>
          <v-col align="left">
            <img src="/oy-logo.png" alt="Ocean Youth Logo" class="logo"
          /></v-col>
        </v-row>
      </v-col>

      <v-col cols="12" sm="6" class="d-flex flex-column justify-center align-center">
        <div class="text-center">
          <h2 class="tagline">
            The inspiring way
            <template v-if="!xs">
              <br />to become an ocean champion and <br />protect our blue planet
            </template>
            <template v-else>
              <br />to become an ocean <br />champion and protect our <br />blue planet
            </template>
          </h2>
          <div class="buttons">
            <v-btn
              id="register-button"
              class="bg-primaryPink text-creamyWhite"
              rounded="xl"
              size="x-large"
              @click="openRegisterModal"
            >
              Get Started
            </v-btn>
            <v-btn
              id="login-button"
              class="bg-primaryBlue text-creamyWhite"
              rounded="xl"
              size="x-large"
              @click="openLoginModal"
            >
              I already have an account
            </v-btn>
          </div>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.header {
  width: 100%;
  height: 200px;
  position: relative;
  overflow: hidden;
  flex-grow: 0;
  flex-shrink: 1;
}

.header-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: boxed;
}

.logo {
  width: 100%;
  max-width: 250px;
}

.buttons {
  display: flex;
  flex-direction: column;
  gap: 60px;
  margin: 50px auto;
}
</style>
