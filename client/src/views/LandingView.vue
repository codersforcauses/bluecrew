<script setup lang="ts">
import { useModalStore } from '@/stores/modal'
import { useDisplay } from 'vuetify'

const { xs } = useDisplay()
const modalStore = useModalStore()

function openRegisterButton() {
  modalStore.openRegister()
}
</script>

<template>
  <div v-if="!xs" class="header">
    <img src="/beach-header.jpg" alt="Ocean Beach" class="header-image" />
  </div>
  <v-row>
    <v-col :cols="xs ? 12 : 6" class="d-flex justify-center align-center">
      <img src="/bc-logo.png" alt="Blue Crew Logo" />
    </v-col>

    <v-col :cols="xs ? 12 : 6" class="d-flex flex-column justify-center align-center">
      <div class="text-center">
        <h2 class="tagline">
          The inspiring way to become an ocean champion and protect our blue planet
        </h2>
        <div class="buttons">
          <v-btn
            id="register-button"
            class="bg-primaryPink text-creamyWhite"
            rounded="xl"
            size="x-large"
            @click="openRegisterButton"
          >
            Get Started
          </v-btn>
          <v-btn
            id="login-button"
            class="bg-primaryBlue text-creamyWhite"
            rounded="xl"
            size="x-large"
            @click="openRegisterButton"
          >
            I already have an account
          </v-btn>
        </div>
      </div>
    </v-col>
  </v-row>
</template>

<style scoped>
.header {
  width: 100%;
  height: 200px;
  position: relative;
  overflow: hidden;
  margin-bottom: 50px;
}

.header-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: boxed;
}

.content-section {
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.buttons {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 400px;
  margin: 20px auto;
}
</style>
