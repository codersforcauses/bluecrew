<script setup lang="ts">
import LeaderboardRow from '@/components/LeaderboardRow.vue'
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

interface LeaderboardApiEntry {
  username: string
  total_points: number
  rank: number
}

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
const error = ref<string | null>(null)

const fetchLeaderboard = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/leaderboard/')
    if (!response.ok) {
      throw new Error('Failed to fetch leaderboard data')
    }
    const apiData: LeaderboardApiEntry[] = await response.json()

    if (userStore.isLoggedIn && apiData.length > 0) {
      // Get current user data from the last entry
      const currentUserData = apiData[apiData.length - 1]
      currentUser.value = {
        rank: currentUserData.rank,
        avatarIndex: currentUserData.avatar,
        name: currentUserData.username,
        points: currentUserData.total_points,
        isHighlighted: true,
      }

      // Get other users excluding the current user
      const otherUsers = apiData.slice(0, -1)
      leaderboardData.value = otherUsers.map((entry) => ({
        rank: entry.rank,
        avatarIndex: entry.avatar,
        name: entry.username,
        points: entry.total_points,
        isHighlighted: false,
      }))
    } else {
      // If not logged in, show all users
      leaderboardData.value = apiData.map((entry) => ({
        rank: entry.rank,
        avatarIndex: entry.avatar,
        name: entry.username,
        points: entry.total_points,
        isHighlighted: false,
      }))
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'An error occurred'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchLeaderboard()
})
</script>

<template>
  <v-container>
    <h2 class="leaderboard-text text-primaryPink mb-4 mb-sm-3 mb-md-4">Leaderboard</h2>

    <div v-if="isLoading" class="text-center pa-4">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>

    <div v-else-if="error" class="text-center error--text pa-4">
      {{ error }}
    </div>

    <template v-else>
      <!-- Your Rank - Only show if logged in and current user exists -->
      <template v-if="userStore.isLoggedIn && currentUser">
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
.leaderboard-text {
  text-align: center;
  font-family: 'Lilita One', cursive;
  font-size: 40px;
  font-weight: 500;
}

.leaderboard-scroll {
  max-height: 400px;
  overflow-y: auto;
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
