<script setup lang="ts">
import { useModalStore } from '@/stores/modal'
import RegisterModal from '@/components/RegisterModal.vue'
import { useDisplay } from 'vuetify'

const modalStore = useModalStore()
const { xs } = useDisplay()

function openRegisterButton() {
  modalStore.openRegister()
}
</script>

<template>
  <div class="landing-page">
    <!-- Desktop Version -->
    <template v-if="!xs">
      <div class="header">
        <img src="/beach-header.jpg" alt="Ocean Beach" class="header-image"/>
      </div>
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
      </div>
    </template>

    <!-- Mobile Version -->
    <template v-else>
      <div class="mobile-overlay">
        <div class="mobile-content">
          <div class="mobile-close">
            <v-icon>mdi-close</v-icon>
          </div>
          <div class="mobile-logo">
            <img src="/bc-logo.png" alt="Blue Crew Logo" />
          </div>
          <h2 class="mobile-tagline text-center">
            The inspiring way to become an ocean champion and protect our blue planet
          </h2>
          <div class="mobile-buttons">
            <v-btn
              block
              class="bg-primaryPink text-creamyWhite mb-4"
              rounded="xl"
              size="x-large"
              @click="openRegisterButton"
            >
              Get Started
            </v-btn>
            <v-btn
              block
              class="bg-primaryBlue text-creamyWhite"
              rounded="xl"
              size="x-large"
              @click="openRegisterButton"
            >
              I already have an account
            </v-btn>
          </div>
        </div>
      </div>
    </template>

    <RegisterModal v-if="modalStore.currentModal === 'register'" @close="modalStore.closeModal" />
  </div>
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

/* Mobile Styles */
.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: white;
  z-index: 1000;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.mobile-content {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
}

.mobile-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  cursor: pointer;
}

.mobile-logo {
  width: 150px;
  margin: 2rem auto;
}

.mobile-logo img {
  width: 100%;
  height: auto;
}

.mobile-tagline {
  text-align: center;
  margin: 2rem 0;
}

.mobile-buttons {
  margin-top: 2rem;
}
</style>
  