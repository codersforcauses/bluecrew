<script setup lang="ts">
  import { ref } from "vue";
  import ChallengesCard from "@/components/ChallengesCard.vue";
  
  const title = ref("Challenge 1");
  const description = ref("This is a challenge");
  const type = ref<'connect' | 'understand' | 'act'>('connect');
  const points = ref(200);
  const startDate = ref("27/11/2024 9:27pm");
  const finishDate = ref("27/11/2024 10:27pm");
  const status = ref<'complete' | 'uncomplete'>('complete');
</script>

<template>
    <v-container>
      <ChallengesCard
        :title="title"
        :description="description"
        :type="type"
        :points="points"
        :startDate="startDate"
        :finishDate="finishDate"
        :status="status"
      />
    </v-container>
  </template>oh
  