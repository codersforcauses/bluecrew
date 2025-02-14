<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useDisplay } from 'vuetify'
import { useUserStore } from '@/stores/user'
import { useModalStore } from '@/stores/modal'
import { useRouter } from 'vue-router'
import ChallengeInteraction from '@/components/ChallengeInteraction.vue'
import WaveBanner from '@/components/WaveBanner.vue'
import avatarPaths from '@/utils/avatar'
import { mockUsers, currentUserData } from '@/utils/mockdata' //for testing
import type { User } from '@/types/user'

// types
interface Challenge {
  title: string
  description: string
  type: 'Connect' | 'Understand' | 'Act'
  points: number
  startDate: string
  finishDate?: string
  status: 'Complete' | 'In Progress'
}

interface UserWithChallenges extends User {
  challenges: Challenge[]
}

const props = defineProps<{
  username?: string
}>()

const { xs } = useDisplay()
const userStore = useUserStore()
const modalStore = useModalStore()
const router = useRouter()
const profileData = ref<UserWithChallenges | null>(null) //data for the profile
userStore.userData = currentUserData //for testing

const initializeProfile = () => {
  if (!userStore.isLoggedIn) {
    modalStore.openLogin()
    router.push('/')
    return
  } //if user is not logged in, open login modal

  if (props.username) {
    const userData = mockUsers[props.username]
    if (userData) {
      profileData.value = userData
    } else {
      router.push('/404')
    }
  } else {
    profileData.value = currentUserData
  }
}

onMounted(() => {
  initializeProfile()
})
</script>

<template>
  <v-container v-if="profileData" fluid class="pa-0 d-flex flex-column">
    <!-- Wave Banner Header -->
    <v-row v-if="!xs" class="header">
      <WaveBanner imageSrc="/teambuilding-background.jpg" />
      <img src="/teambuilding-background.jpg" alt="Ocean Beach" class="header-image" />
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
        <h2 class="text-h6 font-weight-bold mb-4">Challenges</h2>
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
