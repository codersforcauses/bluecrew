<script setup lang="ts">
import { ref } from 'vue'

const show = ref(false);

  defineProps<{
    title: string
    description: string
    type: 'Connect' | 'Understand' | 'Act'
    points: number
    startDate: string
    finishDate: string
    status: 'Complete' | 'In Progress'
  }>()

</script>
<template>
  <v-card class="pa-4 bg-primaryBrown challenge-row"  outlined>
    <v-card-title class="d-flex justify-space-between align-center">
      <div>
        <span class="font-weight-bold text-h6">{{ title }}</span>
        <span class="subtitle ml-2 text-subtitle-2">{{ type }}</span>
      </div>
      <div class="d-flex flex-column">
        <span class="ml-auto pr-5 text-body-1 font-weight-bold">{{ points }}pts</span>
      </div>
    </v-card-title>

    <v-card-text class="d-flex justify-space-between align-center">
      <div class="details">
        <p>
          {{ description }}
        </p>
        <p class="mb-2">
          <strong>Start Date:</strong> {{ startDate }}
        </p>
        <p>
          <strong>Finish Date:</strong> {{ finishDate }}
        </p>
      </div>
      <div>
        <v-chip :class="[status === 'Complete' ? 'bg-success' : 'bg-lightBlue']" text-color="white" class="status-indicator align-self-center mb-15" outlined>
          {{ status }}
        </v-chip>
      </div>
    </v-card-text>

    <div v-if="status === 'Complete'" class="d-flex justify-end mt-n15">
      <v-btn
      color="primaryBlue"
      variant="flat"
      @click="show = !show">
      {{ show ? 'Hide Evidence' : 'Show Evidence' }}
      </v-btn>
    </div>

    <v-expand-transition>
      <div v-show="show">
        <v-divider class="my-1"/>
        <v-card-text>
          <v-img
          width="100%"
          cover
          src=teambuilding-background.jpg
        />
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
  border-color: #4a4a4a ;
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
</style>