<template>
  <v-card class="pa-4" outlined>
    <v-card-title class="d-flex justify-space-between align-center">
      <div>
        <span class="font-weight-bold text-h6">{{ title }}</span>
        <span class="subtitle ml-2 text-subtitle-2">{{ subtitle }}</span>
      </div>
      <span class="text-body-1 font-weight-bold">{{ points }}pts</span>
    </v-card-title>

    <v-card-text class="d-flex justify-space-between align-center">
      <div class="details">
        <p class="mb-2">
          <strong>Complete Date:</strong> {{ completeDate }}
        </p>
        <p>
          <strong>Time Spent on Challenge:</strong> {{ timeSpent }}
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

<script lang="ts">
export default {
  name: "ChallengeCard",
  props: {
    title: {
      type: String,
      default: "Challenge 1",
    },
    subtitle: {
      type: String,
      default: "Bingo 1",
    },
    points: {
      type: Number,
      default: 200,
    },
    completeDate: {
      type: String,
      default: "27/11/2024 10:27pm",
    },
    timeSpent: {
      type: String,
      default: "60min",
    },
    status: {
      type: String,
      default: "Complete",
    },
  },
};
</script>

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
