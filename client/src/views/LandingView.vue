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
  <v-container>
    <v-row
    height="100%">
      <v-col 
      :cols="xs ? 12 : 6" 
      class="d-flex justify-center align-center">
        <img 
        src="/bc-logo.png" 
        alt="Blue Crew Logo" 
        :class="{
        'logo-mobile': xs,
        'logo-desktop': !xs
        }"/>
        <img 
        src="/oy-logo.png" 
        alt="Ocean Youth Logo" 
        :class="{
        'logo-mobile': xs,
        'logo-desktop': !xs
        }"/>
      </v-col>

      <v-col 
      :cols="xs ? 12 : 6" 
      class="d-flex flex-column justify-center align-center">
        <div class="text-center">
          <h2 class="tagline">
            The inspiring way
            <template v-if="!xs">
              <br>to become an ocean champion and
              <br>protect our blue planet
            </template>
            <template v-else>
              <br>to become an ocean
              <br>champion and protect our
              <br>blue planet
            </template>
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
  </v-container>
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

.logo-mobile {
  width: 150px;
  margin: 40px 20px;
}

.logo-desktop {
  width: 250px;
  margin: 0 20px;
}

.buttons {
  display: flex;
  flex-direction: column;
  gap: 60px;
  max-width: 400px;
  margin: 50px auto;
}
</style>
