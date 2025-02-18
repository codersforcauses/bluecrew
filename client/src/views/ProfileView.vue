<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useDisplay } from 'vuetify'
import { useUserStore } from '@/stores/user'
import { useModalStore } from '@/stores/modal'
import { useRouter } from 'vue-router'
import ChallengeInteraction from '@/components/ChallengeInteraction.vue'
import WaveBanner from '@/components/WaveBanner.vue'
import avatarPaths from '@/utils/avatar'
import server from '@/utils/server'
import { useMessageStore } from '@/stores/message'
import type { AxiosError } from 'axios'
import type { Challenge, UserProfile } from '@/types/profile'

const props = defineProps<{
  username?: string
}>()

const { xs } = useDisplay()
const userStore = useUserStore()
const modalStore = useModalStore()
const messageStore = useMessageStore()
const router = useRouter()
const profileData = ref<UserProfile | null>(null) // data for the profile
const challengeData = ref<Challenge[] | null>(null)
const permission = ref(false)
const loading = ref(true)

const profileUserName = computed(() => {
  if (props.username) {
    return props.username
  } else if (userStore.userData !== null) {
    return userStore.userData.userName
  } else {
    return ''
  }
})

const initializeProfile = () => {
  if (!userStore.isLoggedIn && !props.username) {
    modalStore.openLogin()
    router.push('/')
    return
  } //if user is not logged in, open login modal

  server
    .get(`/get-profile-page/${profileUserName.value}/`)
    .then((res) => {
      profileData.value = res.data.user_info as UserProfile
      challengeData.value = res.data.challenges as Challenge[]
      permission.value = res.data.permission
      loading.value = false
    })
    .catch((error: AxiosError) => {
      loading.value = false
      if (error.response?.status === 404) {
        messageStore.showMessage(
          'Not Found',
          `User "${profileUserName.value}" was not found.`,
          'warning',
        )
      } else {
        messageStore.showMessage(
          'Error',
          'Unexpected occured while fetching user profile.',
          'error',
        )
      }
    })
}

onMounted(() => {
  initializeProfile()
})
</script>

<template>
  <div v-if="loading" class="d-flex align-center justify-center h-100">
    <v-progress-circular indeterminate color="primaryBlue" />
  </div>
  <v-container v-else-if="profileData !== null" fluid class="pa-0 d-flex flex-column">
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

        <p class="text-h4 font-weight-bold mb-1">{{ profileUserName }}</p>
        <h3 class="text-h6 mb-1">{{ profileData.firstName }} {{ profileData.lastName }}</h3>
        <p class="mb-1">{{ profileData.bio }}</p>
        <p class="text-body-1">Total Points: {{ profileData.totalPoints }} pts</p>
      </v-col>
    </v-row>

    <!-- Challenges Section -->
    <v-row class="px-4 px-sm-16 mx-0">
      <v-col cols="12">
        <h2 class="text-h6 font-weight-bold mb-4">Challenges</h2>
        <p v-if="!permission" class="text-red">
          You do not have permission to view this person's challenges.
        </p>
        <p v-else-if="challengeData && challengeData.length === 0">No challenges started yet.</p>
        <div v-else class="d-flex flex-column gap-4">
          <ChallengeInteraction
            v-for="challenge in challengeData"
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
