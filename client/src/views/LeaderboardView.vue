<template>
  <v-container class="custom-container">
    <WaveHeader imageSrc="/teambuilding-background.jpg" />
  </v-container>
  <v-container>
    <h2 class="leaderboard-text text-primaryPink mb-4 mb-sm-3 mb-md-4">Leaderboard</h2>

    <!-- Your Rank -->
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
  </v-container>
</template>

<script setup lang="ts">
import LeaderboardRow from '@/components/LeaderboardRow.vue'
import WaveHeader from '@/components/WaveHeader.vue'
import { ref } from 'vue'

// Define TypeScript interface for leaderboard data
interface LeaderboardEntry {
  rank: number
  avatarIndex: number
  name: string
  points: number
  isHighlighted: boolean
}

const leaderboardData = ref<LeaderboardEntry[]>([
  { rank: 1, avatarIndex: 2, name: 'Marsha Fisher', points: 36, isHighlighted: false },
  { rank: 2, avatarIndex: 3, name: 'Juanita Cormier', points: 35, isHighlighted: false },
  { rank: 3, avatarIndex: 3, name: 'You', points: 34, isHighlighted: true },
  { rank: 4, avatarIndex: 1, name: 'Tamara Schmidt', points: 33, isHighlighted: false },
  { rank: 5, avatarIndex: 4, name: 'Ricardo Veum', points: 32, isHighlighted: false },
])

const currentUser = ref<LeaderboardEntry>({
  rank: 3,
  avatarIndex: 3,
  name: 'You',
  points: 34,
  isHighlighted: true,
})
</script>

<style scoped>
.custom-container {
  max-width: 100% !important;
  padding: 0 !important;
}

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
