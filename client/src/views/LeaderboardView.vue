# LeaderboardView.vue
<script setup lang="ts">
import LeaderboardRow from '@/components/LeaderboardRow.vue'
import WaveBanner from '@/components/WaveBanner.vue'
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useMessageStore } from '@/stores/message'
import server from '@/utils/server'
import type { ExtendedAxiosError } from '@/types/other'

// What we receive from the API
interface LeaderboardApiEntry {
  username: string
  total_points: number
  rank: number
  avatar: number
}

// What we use in our component
interface LeaderboardEntry {
  rank: number
  avatarIndex: number
  name: string
  points: number
  isHighlighted: boolean
}

const userStore = useUserStore()
const leaderboardData = ref<LeaderboardEntry[]>([])
const currentUser = ref<LeaderboardEntry | null>(null)
const isLoading = ref(true)
const messageStore = useMessageStore()

const transformEntry = (
  entry: LeaderboardApiEntry,
  highlight: boolean = false,
): LeaderboardEntry => ({
  rank: entry.rank,
  avatarIndex: entry.avatar,
  name: entry.username,
  points: entry.total_points,
  isHighlighted: highlight,
})

const fetchLeaderboard = async () => {
  isLoading.value = true
  server
    .get<LeaderboardApiEntry[]>('/leaderboard/', {
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
    .then((response) => {
      const data = response.data
      if (userStore.normalUserLoggedIn && data.length > 0) {
        const currentUserData = data[data.length - 1]
        currentUser.value = transformEntry(currentUserData, true)
        // Transform the data immediately when assigning
        leaderboardData.value = data.slice(0, -1).map((entry) => transformEntry(entry))
      } else {
        // Not logged in, show all entries
        leaderboardData.value = data.map((entry) => transformEntry(entry))
      }
    })
    .catch((error: ExtendedAxiosError) => {
      messageStore.handleUnexpectedError(error.config?.session_expired, false)
    })
    .finally(() => {
      isLoading.value = false
    })
}

onMounted(() => {
  fetchLeaderboard()
})
</script>

<template>
  <WaveBanner
    imageSrc="/blue-crew-group.jpg"
    altText="Volunteers standing on a beach with seaweed"
  />
  <v-container>
    <h2 class="leaderboard-text text-primaryGreen mb-4 mb-sm-3 mb-md-4">Leaderboard</h2>

    <div v-if="isLoading" class="text-center pa-4">
      <v-progress-circular indeterminate color="primaryBlue" />
    </div>

    <template v-else>
      <!-- Your Rank - Only show if logged in, current user exists, and not a superuser -->
      <template v-if="userStore.normalUserLoggedIn && currentUser">
        <h3 class="section-title text-primaryBlue">Your Rank</h3>
        <v-row>
          <v-col cols="12">
            <LeaderboardRow
              :rank="currentUser.rank"
              :avatar-index="currentUser.avatarIndex"
              :name="currentUser.name"
              :points="currentUser.points"
              :is-highlighted="true"
            />
          </v-col>
        </v-row>
      </template>

      <!-- Other Users -->
      <h3 class="section-title2 text-primaryBlue">Overall Rankings</h3>
      <v-row class="leaderboard-scroll">
        <v-col v-for="(row, index) in leaderboardData" :key="index" cols="12">
          <LeaderboardRow
            :rank="row.rank"
            :avatar-index="row.avatarIndex"
            :name="row.name"
            :points="row.points"
            :is-highlighted="row.isHighlighted"
          />
        </v-col>
      </v-row>
    </template>
  </v-container>
</template>

<style scoped>
.custom-container {
  max-width: 100%;
  padding: 0;
}

.leaderboard-text {
  text-align: center;
  font-family: 'Lilita One', cursive;
  font-size: 40px;
  font-weight: 500;
}

.leaderboard-scroll {
  scrollbar-width: thin;
}

.section-title {
  margin-top: 16px;
  margin-bottom: 2px;
  font-size: 20px;
  font-family: 'Poppins', cursive;
  text-align: left;
  font-weight: bold;
}

.section-title2 {
  margin-top: 32px;
  margin-bottom: 2px;
  font-size: 20px;
  font-family: 'Poppins', cursive;
  text-align: left;
  font-weight: bold;
}
</style>
