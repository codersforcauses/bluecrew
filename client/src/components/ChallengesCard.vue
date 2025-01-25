<script setup lang="ts">

  defineProps<{
    title: string
    description: string
    type: 'connect' | 'understand' | 'act'
    points: number
    startDate: string
    finishDate: string
    status: 'complete' | 'uncomplete'
  }>()
</script>

<template>
  <v-card class="pa-4" outlined>
    <v-card-title class="d-flex justify-space-between align-center">
      <div>
        <span class="font-weight-bold text-h6">{{ title }}</span>
        <span class="subtitle ml-2 text-subtitle-2">{{ description }}</span>
      </div>
      <span class="text-body-1 font-weight-bold">{{ points }}pts</span>
    </v-card-title>

    <v-card-text class="d-flex justify-space-between align-center">
      <div class="details">
        <p class="mb-2">
          <strong>Complete Date:</strong> {{ finishDate }}
        </p>
        <p>
          <strong>Start Date:</strong> {{ startDate }}
        </p>
      </div>
      <v-chip
        color="success"
        text-color="white"
        class="status-indicator"
        outlined
      >
        ✔ {{ status }}
      </v-chip>
    </v-card-text>
  </v-card>
</template>

<style scoped>
.subtitle {
  color: #6b6b6b;
  font-size: 14px;
}
.details p {
  margin: 4px 0;
  font-size: 14px;
  color: #4a4a4a;
}
</style>