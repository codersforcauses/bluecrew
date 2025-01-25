<script setup lang="ts">

  defineProps<{
    title: string
    description: string
    type: 'Connect' | 'Understand' | 'Act'
    points: number
    startDate: string
    finishDate: string
    status: 'Complete' | 'Uncomplete'
  }>()
</script>

<template>
  <v-card class="pa-4 bg-primaryBrown" outlined>
    <v-card-title class="d-flex justify-space-between align-center">
      <div>
        <span class="font-weight-bold text-h6">{{ title }}</span>
        <span class="subtitle ml-2 text-subtitle-2">{{ type }}</span>
      </div>
      <span class="text-body-1 font-weight-bold">{{ points }}pts</span>
      <div>
        <v-chip color="success" text-color="white" class="status-indicator" outlined>
          ✔ {{ status }}
        </v-chip>
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
      
    </v-card-text>
  </v-card>
</template>

<style scoped>
.subtitle {
  color: #6b6b6b;
  font-size: 14px;
  font-family: poppins;
}
.details p {
  margin: 4px 0;
  font-size: 14px;
  color: #4a4a4a;
  font-family: poppins;
}
</style>