<script setup lang="ts">
import { ref, computed } from 'vue'
import { useDisplay } from 'vuetify'
import { useUserStore } from '@/stores/user'
import type { ChallengeInfo } from '@/types/challenge'
import BingoTile from '@/components/BingoTile.vue'
import ChallengeCard from '@/components/ChallengeCard.vue'
import WaveBanner from '@/components/WaveBanner.vue'

const { xs } = useDisplay()
const userStore = useUserStore()

const containerClass = computed(() => (!xs.value ? 'desktop-container' : 'mobile-container'))

// Define all challenge info objects
const challengeInfos = ref<ChallengeInfo[]>([
  {
    title: 'Watch an Ocean Documentary',
    points: 200,
    type: 'understand',
    description: 'Here are some of our top picks! You can choose one of them or watch one of your own. Tell us what you thought and submit a picture.',
    status: 'not started'
  },
  // Add more challenges to fill all 16 tiles
  ...Array(15).fill({
    title: 'Ocean Challenge',
    points: 100,
    type: 'connect',
    description: 'placeholder text',
    status: 'not started'
  })
])

const selectedTile = ref<number | null>(null)
const showChallengeCard = ref(false)
const currentChallenge = ref<ChallengeInfo>(challengeInfos.value[0])

const handleTileClick = (index: number) => {
  selectedTile.value = index
  currentChallenge.value = challengeInfos.value[index]
  showChallengeCard.value = true
}

const handleCloseChallenge = () => {
  showChallengeCard.value = false
  selectedTile.value = null
}

const handleStatusChange = (newStatus: 'not started' | 'started' | 'completed') => {
  if (selectedTile.value !== null) {
    challengeInfos.value[selectedTile.value].status = newStatus
    currentChallenge.value.status = newStatus
  }
}
</script>

<template>
  <WaveBanner imageSrc="/homepage-scaled.jpg" />

  <div :class="['content-wrapper', containerClass]">
    <!-- Desktop Version -->
    <template v-if="!xs">
      <div class="desktop-layout">
        <div class="left-section">
          <!-- Header Section -->
          <div class="header-section desktop-header">
            <h1 class="blingo-title text-primaryBlue">Blingo</h1>
            <h2 class="blingo-subtitle text-primaryGreen">Connecting to the ocean</h2>
          </div>

          <!-- Challenge Card -->
          <div v-if="showChallengeCard" class="challenge-card-container desktop-challenge-card">
            <ChallengeCard v-bind="currentChallenge" :is-logged-in="userStore.isLoggedIn" @close="handleCloseChallenge"
              @status-change="handleStatusChange" />
          </div>

          <!-- Learn More Section -->
          <div class="learn-more-section text-primaryGreen">
            <p class="learn-more-title">Want to learn more?</p>
            <p class="learn-more-text">
              Head to
              <a href="https://bluecrew.com.au/" class="text-link">https://bluecrew.com.au/</a>
            </p>
            <p class="learn-more-text">
              and
              <a href="https://www.oceanyouth.org/" class="text-link">https://www.oceanyouth.org/</a>
            </p>
          </div>
        </div>

        <!-- Game Grid -->
        <div class="game-grid desktop-game-grid">
          <div class="grid-row" v-for="row in 4" :key="`row-${row}`">
            <div v-for="col in 4" :key="`tile-${row}-${col}`" class="tile-wrapper">
              <BingoTile v-bind="challengeInfos[(row - 1) * 4 + (col - 1)]"
                :selected="selectedTile === (row - 1) * 4 + (col - 1)"
                @click="handleTileClick((row - 1) * 4 + (col - 1))" />
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Mobile Layout -->
    <template v-else>
      <!-- Title Section -->
      <div class="header-section mobile-header">
        <h1 class="blingo-title text-primaryBlue">Blingo</h1>
        <h2 class="blingo-subtitle text-primaryGreen">Connecting to the ocean</h2>
      </div>

      <!-- Game Grid -->
      <div class="game-grid">
        <div class="grid-row" v-for="row in 4" :key="`row-${row}`">
          <div v-for="col in 4" :key="`tile-${row}-${col}`" class="tile-wrapper">
            <BingoTile v-bind="challengeInfos[(row - 1) * 4 + (col - 1)]"
              :selected="selectedTile === (row - 1) * 4 + (col - 1)"
              @click="handleTileClick((row - 1) * 4 + (col - 1))" />
          </div>
        </div>
      </div>

      <!-- Learn More Section -->
      <div class="learn-more-section text-primaryGreen mt-8">
        <p class="learn-more-title">Want to learn more?</p>
        <p class="learn-more-text">
          Head to <a href="https://bluecrew.com.au/" class="text-link">https://bluecrew.com.au/</a>
        </p>
        <p class="learn-more-text">
          and
          <a href="https://www.oceanyouth.org/" class="text-link">https://www.oceanyouth.org/</a>
        </p>
      </div>

      <!-- Challenge Card -->
      <div v-if="showChallengeCard" class="challenge-card-overlay">
        <ChallengeCard v-bind="currentChallenge" :is-logged-in="userStore.isLoggedIn" @close="handleCloseChallenge"
          @status-change="handleStatusChange" />
      </div>
    </template>
  </div>
</template>

<style scoped>
.content-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  padding: 1.25rem;
  font-family: 'Poppins', sans-serif;
}

.header-section {
  margin-bottom: 1.5rem;
}

.blingo-title {
  font-family: 'Lilita One', cursive;
  text-align: center;
}

.blingo-subtitle {
  text-align: center;
}

.desktop-challenge-card {
  max-width: 60%;
  margin: 0 auto;
}

/* Learn More Section */
.learn-more-section {
  text-align: center;
}

.learn-more-title {
  font-weight: bold;
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.learn-more-text {
  font-weight: bold;
  margin: 0.5rem 0;
  font-size: 1rem;
}

/* Challenge Card Overlay for Mobile */
.challenge-card-overlay {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  width: 100%;
  max-width: 90vw;
  display: flex;
  justify-content: center;
}

.challenge-card-overlay::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: -1;
}

/* Grid Layout */
.game-grid {
  width: 100%;
}

.grid-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.25rem;
}

.tile-wrapper {
  flex: 1;
  margin: 0 0.125rem;
  position: relative;
}

/* Mobile Layout */
.mobile-container {
  flex-direction: column;
  padding: 1.25rem;
}

.mobile-container .blingo-title {
  font-size: 2.5rem;
}

.mobile-container .blingo-subtitle {
  font-size: 1.25rem;
}

/* Desktop Layout */
.desktop-layout {
  display: flex;
  justify-content: space-between;
  align-items: stretch;
  width: 100%;
  padding: 2rem;
}

.desktop-header .blingo-title {
  font-size: 3rem;
}

.desktop-header .blingo-subtitle {
  font-size: 1.5rem;
}

.desktop-game-grid {
  flex: 1;
  max-width: 40%;
}

.left-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 100%;
}
</style>