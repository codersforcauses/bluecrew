<script setup lang="ts">
import { useModalStore } from '@/stores/modal'
import RegisterModal from '@/components/RegisterModal.vue'

const modalStore = useModalStore()

function openRegisterButton() {
  modalStore.openRegister()
}
//import { useDisplay } from 'vuetify' // Used to figure out if page is landscape/portrait
</script>

<template>
  <div class="landing-page">
    <!-- Top Image Section -->
    <div class="header">
      <img src="/beach-header.jpg" alt="Ocean Beach" class="header-image"/>
    </div>

    <!-- Content Section -->
    <div class="content-section">
      <div class="logo">
        <img src="/bc-logo.png" alt="Blue Crew Logo" />
      </div>
      <div class="info-box">
        <h2 class="tagline">
          The inspiring way to become an ocean champion and protect our blue planet
        </h2>
        <div class="buttons">
          <v-btn
            id="register-button"
            class="bg-primaryPink text-creamyWhite d-flex justify-center align-center"
            rounded="xl"
            size="x-large"
            @click="openRegisterButton"
          >
            Get Started
          </v-btn>
          <RegisterModal v-if="modalStore.currentModal === 'register'" @close="modalStore.closeModal" />
          <v-btn
            id="login-button"
            class="bg-primaryBlue text-creamyWhite d-flex justify-center align-center"
            rounded="xl"
            size="x-large"
            @click="openRegisterButton"
          >
            I already have an account
          </v-btn>
          <RegisterModal v-if="modalStore.currentModal === 'register'" @close="modalStore.closeModal" /> <!--Needs to be changed to login button-->>
        </div>
      </div>
    </div>
  </div>
</template>
  

<style scoped>
.header {
  width: 100%;
  height: 200px; /* Adjust height as needed */
  position: relative;
  overflow: hidden;
  margin-bottom: 50px;
}

.header-image {
  width: 100%;
  height: 100%;
  object-fit: cover; /* Makes image cover the container */
  display: block;
}

.content-section {
  display: flex;
  justify-content: space-around;
  align-items: center;
}
</style>
  