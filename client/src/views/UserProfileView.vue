<!-- views/UserProfileView.vue -->
<script setup lang="ts">
import { ref } from 'vue'
import ChallengeInteraction from '@/components/ChallengeInteraction.vue'
import WaveBanner from '@/components/WaveBanner.vue'
import { useDisplay } from 'vuetify'
import { useUserStore } from '@/stores/user'
import avatarPaths from '@/utils/avatar'

const props = defineProps<{
  username?: string
}>()

const { xs } = useDisplay()
const userStore = useUserStore()

// 模拟数据
const profileData = ref({
  userName: 'Username',
  firstName: 'Firstname',
  lastName: 'Lastname',
  bio: 'This is a bio.',
  totalPoints: 2000,
  avatar: 0,
  challenges: [
    {
      title: 'Challenge 1',
      description: 'Bingo 1 Challenge Description',
      type: 'Connect' as const,
      points: 200,
      startDate: '27/11/2024 10:27pm',
      finishDate: '27/11/2024 11:27pm',
      status: 'Complete' as const,
    },
  ],
})
</script>

<template>
  <v-container fluid class="pa-0 d-flex flex-column">
    <!-- Wave Banner Header -->
    <v-row v-if="!xs" class="header">
      <WaveBanner imageSrc="/beach-header.jpg" />
      <img src="/beach-header.jpg" alt="Ocean Beach" class="header-image" />
    </v-row>

    <!-- Profile Content -->
    <v-row class="px-4 px-sm-16 mx-0">
      <v-col cols="12" class="d-flex flex-column">
        <!-- Avatar and Basic Info -->
        <div class="d-flex align-start mb-4">
          <v-img
            class="rounded-circle"
            max-height="96"
            max-width="96"
            min-width="96"
            contain
            :src="avatarPaths[profileData.avatar]"
          />
        </div>

        <p class="text-h4 font-weight-bold mb-1">{{ profileData.userName }}</p>
        <h3 class="text-h6 mb-1">{{ profileData.firstName }} {{ profileData.lastName }}</h3>
        <p class="mb-1">{{ profileData.bio }}</p>
        <p class="text-body-1">Total Points: {{ profileData.totalPoints }} pts</p>
      </v-col>
    </v-row>

    <!-- Challenges Section -->
    <v-row class="px-4 px-sm-16 mx-0">
      <v-col cols="12">
        <h2 class="text-h6 font-weight-bold mb-4">Challenge Complete</h2>
        <div class="d-flex flex-column gap-4">
          <ChallengeInteraction
            v-for="challenge in profileData.challenges"
            :key="challenge.title"
            v-bind="challenge"
          />
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
}

.header-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

h3 {
  color: rgb(var(--v-theme-primaryGreen));
}

.gap-4 {
  gap: 16px;
}
</style>
