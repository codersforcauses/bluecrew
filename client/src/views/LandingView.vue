<script setup lang="ts">
import WaveBanner from '@/components/WaveBanner.vue'
import { useModalStore } from '@/stores/modal'
import { useDisplay } from 'vuetify'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const { xs } = useDisplay()
const modalStore = useModalStore()
const userStore = useUserStore()
const router = useRouter()

const openRegisterModal = () => {
  modalStore.openRegister()
}

const openLoginModal = () => {
  modalStore.openLogin()
}

const goToBingoPage = () => {
  router.push({ name: 'blingo' })
}
</script>

<template>
  <v-container fluid class="fill-height pa-0 flex-column" :class="{ 'mt-14': xs }">
    <v-row v-if="!xs">
      <v-container class="pa-0">
        <WaveBanner imageSrc="/colourful-coral.png" altText="Colourful coral" />
      </v-container>
    </v-row>
    <v-row class="flex-grow-1 w-100" align="center">
      <v-col cols="12" sm="6" align-self="center">
        <v-row>
          <v-col align="center"
            ><img src="/blingo-logo.svg" alt="Blingo Logo" class="logo" />
          </v-col>
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
            <template v-if="userStore.isLoggedIn">
              <p class="text-primaryGreen welcome-text">
                Welcome back, {{ userStore.userData?.userName }}.
              </p>
              <v-btn
                id="bingo-button"
                class="bg-primaryBlue text-creamyWhite"
                rounded="xl"
                size="x-large"
                @click="goToBingoPage"
              >
                Go to Blingo
              </v-btn>
            </template>
            <template v-else>
              <v-btn
                id="register-button"
                class="bg-primaryGreen text-creamyWhite"
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
            </template>
          </div>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
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

.welcome-text {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}
</style>
