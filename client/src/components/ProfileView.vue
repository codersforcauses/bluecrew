<template>
    <v-container>
      <ChallengesCard
        :title="title"
        :subtitle="subtitle"
        :points="points"
        :completeDate="completeDate"
        :timeSpent="timeSpent"
        :status="status"
      />
    </v-container>
  </template>oh
  
  <script lang="ts">
  import { defineComponent, ref } from "vue";
  import ChallengesCard from "@/components/ChallengesCard.vue";
  
  export default defineComponent({
    name: "App",
    components: {
        ChallengesCard,
    },
    setup() {
      // Reactive state variables using Composition API
      const title = ref("Challenge 1");
      const subtitle = ref("Bingo 1");
      const points = ref(200);
      const completeDate = ref("27/11/2024 10:27pm");
      const timeSpent = ref("60min");
      const status = ref("Complete");
  
      return {
        title,
        subtitle,
        points,
        completeDate,
        timeSpent,
        status,
      };
    },
  });
  </script>
  