<script setup lang="ts">
import { useDisplay } from 'vuetify'
import { useRouter } from 'vue-router'

const { xs } = useDisplay()
const router = useRouter()

const goHome = () => {
  router.push('/')
}
</script>

<template>
  <v-container fluid class="fill-height pa-0">
    <v-row class="ma-0 align-center justify-center">
      <v-col cols="12" class="d-flex justify-center">
        <div class="text-center">
          <div class="d-flex align-center justify-center mb-4">
            <h1 class="error-code text-primaryBlue">404</h1>
          </div>
          <h2 class="tagline mb-4">
            Uh oh! Page not found
            <template v-if="!xs">
              <br />Looks like you've ventured <br />into uncharted waters
            </template>
          </h2>
          <v-img src="/submarine.png" :max-width="xs ? '60' : '100'" class="mb-2 mx-auto" contain />
          <div class="buttons">
            <v-btn
              id="home-button"
              class="bg-primaryGreen text-creamyWhite"
              rounded="xl"
              size="x-large"
              @click="goHome"
            >
              Go Home
            </v-btn>
          </div>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.error-code {
  font-size: 5rem;
  font-weight: bold;
  line-height: 1.2;
}

.tagline {
  font-size: 2rem;
  line-height: 1.5;
}

.buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 50px 0;
  width: 100%;
}

@media (max-width: 600px) {
  .error-code {
    font-size: 3rem;
  }
  .tagline {
    font-size: 1.5rem;
  }
}
</style>
