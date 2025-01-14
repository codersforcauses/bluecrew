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
  <v-container fluid class="error-container pa-0">
    <v-row class="ma-0">
      <v-col cols="12" class="d-flex justify-center align-center">
        <div class="text-center">
          <h2 class="tagline">
            Uh oh! Page not found
            <template v-if="!xs">
              <br />Looks like you've ventured <br />into uncharted waters
            </template>
            <template v-else">
              <br />Looks like you've <br />ventured into <br />uncharted waters
            </template>
          </h2>
          <div class="buttons">
            <v-btn
              id="home-button"
              class="bg-primaryPink text-creamyWhite"
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
.error-container {
  height: calc(100vh - 144px); 
  display: flex;
  align-items: center;
  justify-content: center;
}

.buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 50px auto;
}

.tagline {
  font-size: 2rem;
  line-height: 1.5;
}

@media (max-width: 600px) {
  .tagline {
    font-size: 1.5rem;
  }
}
</style>