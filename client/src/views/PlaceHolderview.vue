<script setup lang="ts">
import FriendComponent from '@/components/FriendComponent.vue'
import { ref } from 'vue'

// Define TypeScript interface for leaderboard data
interface LeaderboardEntry {
  avatarIndex: number
  name: string
  isHighlighted: boolean
}

const leaderboardData = ref<LeaderboardEntry[]>([
  { avatarIndex: 2, name: 'Marsha Fisher', isHighlighted: false },
  { avatarIndex: 3, name: 'Juanita Cormier', isHighlighted: false },
  { avatarIndex: 1, name: 'Tamara Schmidt', isHighlighted: false },
  { avatarIndex: 4, name: 'Ricardo Veum', isHighlighted: false },
])
</script>

<template>
  <v-container>
    <h2 class="leaderboard-text text-primaryPink mb-4 mb-sm-3 mb-md-4">Friends</h2>

    <!-- Other Users -->
    <h3 class="section-title2 text-primaryBlue">Overall Rankings</h3>
    <v-row class="leaderboard-scroll">
      <v-col v-for="(row, index) in leaderboardData" :key="index" cols="12">
        <FriendComponent
          :avatar-index="row.avatarIndex"
          :name="row.name"
          :is-highlighted="row.isHighlighted"
        />
      </v-col>
    </v-row>
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
