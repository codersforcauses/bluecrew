<script setup lang="ts">
import type { Challenge } from '@/types/profile'
import { ref } from 'vue'

const show = ref(false)
const backendUrl = import.meta.env.VITE_BACKEND_URL

defineProps<Challenge>()
</script>
<template>
  <v-card class="pa-4 mb-2 bg-primaryBrown challenge-row" outlined>
    <div class="d-flex flex-wrap justify-left align-center">
      <p class="ml-4 font-weight-bold text-h6">{{ title }}</p>
      <div class="d-flex flex-grow-1 justify-space-between mr-5 ml-2">
        <p class="subtitle ml-2 text-subtitle-2">{{ type }}</p>
        <p class="text-body-1 font-weight-bold">{{ points }}pts</p>
      </div>
    </div>

    <div class="d-flex flex-column">
      <v-card-text class="d-flex justify-space-between align-center">
        <div class="details">
          <p v-if="description && completed" class="description">
            {{ description }}
          </p>
        </div>
      </v-card-text>

      <div class="d-flex flex-row align-center justify-space-between ml-5 mr-5">
        <div>
          <p class="mb-2"><strong>Start Date:</strong> {{ startDate }}</p>
          <p v-if="completed">
            <strong>Finish Date:</strong>
            {{ finishDate }}
          </p>
        </div>
        <div class="align-center justify-center">
          <v-chip
            :class="[completed ? 'bg-success' : 'bg-lightBlue']"
            text-color="white"
            class="status-indicator align-center"
            outlined
          >
            {{ completed ? 'Complete' : 'In Progress' }}
          </v-chip>
        </div>
      </div>

      <div v-if="completed" class="d-flex justify-center align-center mt-5 mb-2">
        <v-btn color="primaryBlue" variant="flat" @click="show = !show">
          {{ show ? 'Hide Evidence' : 'Show Evidence' }}
        </v-btn>
      </div>
    </div>
    <v-expand-transition>
      <div v-show="show">
        <v-divider class="my-1" />
        <v-card-text>
          <template v-if="image">
            <v-img class="user-image" :src="`${backendUrl}${image}`" />
            <p v-if="imageDescription" class="font-weight-bold mt-4">
              Description: <span class="font-weight-regular">{{ imageDescription }}</span>
            </p>
          </template>
          <p v-else>No evidence found for this challenge :(</p>
        </v-card-text>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<style scoped>
.challenge-row {
  gap: 16px;
  min-height: 50px;
  padding-left: 20px;
  padding-right: 20px;
  align-items: center;
  border-radius: 8px;
  border-width: 1px;
  border-color: #4a4a4a;
}

.subtitle {
  color: #6b6b6b;
  font-size: 14px;
  font-family: poppins;
}

.details p {
  margin-bottom: 15px;
  font-size: 14px;
  color: #4a4a4a;
  font-family: poppins;
}

.user-image {
  max-height: 80vh;
}
</style>
