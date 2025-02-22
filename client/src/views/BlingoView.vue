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
const gridSize = 4

// Define all challenge info objects
const challengeInfos = ref<ChallengeInfo[]>([
  {
    title: 'Watch an Ocean Documentary',
    points: 200,
    type: 'understand',
    description:
      'Here are some of our top picks! You can choose one of them or watch one of your own. Tell us what you thought and submit a picture.',
    status: 'not started',
  },
  {
    title: 'Ocean Challenge',
    points: 100,
    type: 'connect',
    description: 'placeholder text',
    status: 'not started',
  },
  {
    title: 'Ocean Challenge',
    points: 100,
    type: 'connect',
    description: 'placeholder text',
    status: 'not started',
  },
  {
    title: 'Ocean Challenge',
    points: 100,
    type: 'connect',
    description: 'placeholder text',
    status: 'not started',
  },
  {
    title: 'Ocean Challenge',
    points: 100,
    type: 'connect',
    description: 'placeholder text',
    status: 'not started',
  },
  {
    title: 'Ocean Challenge',
    points: 100,
    type: 'connect',
    description: 'placeholder text',
    status: 'not started',
  },
  {
    title: 'Ocean Challenge',
    points: 100,
    type: 'connect',
    description: 'placeholder text',
    status: 'not started',
  },
  {
    title: 'Ocean Challenge',
    points: 100,
    type: 'connect',
    description: 'placeholder text',
    status: 'not started',
  },
  {
    title: 'Ocean Challenge',
    points: 100,
    type: 'connect',
    description: 'placeholder text',
    status: 'not started',
  },
  {
    title: 'Ocean Challenge',
    points: 100,
    type: 'connect',
    description: 'placeholder text',
    status: 'not started',
  },
  {
    title: 'Ocean Challenge',
    points: 100,
    type: 'connect',
    description: 'placeholder text',
    status: 'not started',
  },
  {
    title: 'Ocean Challenge',
    points: 100,
    type: 'connect',
    description: 'placeholder text',
    status: 'not started',
  },
  {
    title: 'Ocean Challenge',
    points: 100,
    type: 'connect',
    description: 'placeholder text',
    status: 'not started',
  },
  {
    title: 'Ocean Challenge',
    points: 100,
    type: 'connect',
    description: 'placeholder text',
    status: 'not started',
  },
  {
    title: 'Ocean Challenge',
    points: 100,
    type: 'connect',
    description: 'placeholder text',
    status: 'not started',
  },
  {
    title: 'Ocean Challenge',
    points: 100,
    type: 'connect',
    description: 'placeholder text',
    status: 'not started',
  },
])

const bingoRows = ref<boolean[]>(Array(gridSize).fill(false))
const bingoCols = ref<boolean[]>(Array(gridSize).fill(false))
const bingoDiagonal = ref<boolean[]>([false, false]) // [↘, ↙]

const checkBingo = () => {
  for (let i = 0; i < gridSize; i++) {
    if (
      challengeInfos.value
        .slice(i * gridSize, (i + 1) * gridSize)
        .every((tile) => tile.status === 'completed')
    ) {
      bingoRows.value[i] = true
    }
    if (
      challengeInfos.value
        .filter((_, index) => index % gridSize === i)
        .every((tile) => tile.status === 'completed')
    ) {
      bingoCols.value[i] = true
    }
  }

  if ([0, 5, 10, 15].every((i) => challengeInfos.value[i].status === 'completed')) {
    bingoDiagonal.value[0] = true // ↘
  }
  if ([3, 6, 9, 12].every((i) => challengeInfos.value[i].status === 'completed')) {
    bingoDiagonal.value[1] = true // ↙
  }
}

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
    checkBingo()
  }
}
</script>

<template>
  <div class="main-container">
    <WaveBanner imageSrc="/homepage-scaled.jpg" />

    <div :class="['content-wrapper', containerClass]">
      <!-- Desktop Version -->
      <template v-if="!xs">
        <div class="desktop-layout">
          <div class="content-container">
            <div class="left-section">
              <!-- Header Section -->
              <div class="header-section desktop-header">
                <h1 class="blingo-title text-primaryBlue">Blingo</h1>
                <h2 class="blingo-subtitle text-primaryGreen">Connecting to the ocean</h2>
              </div>

              <!-- Challenge Card -->
              <div v-if="showChallengeCard" class="challenge-card-container desktop-challenge-card">
                <ChallengeCard
                  v-bind="currentChallenge"
                  :is-logged-in="userStore.isLoggedIn"
                  @close="handleCloseChallenge"
                  @status-change="handleStatusChange"
                />
              </div>

              <!-- Learn More Section (Only for Desktop) -->
              <div class="learn-more-section text-primaryGreen">
                <p class="learn-more-title">Want to learn more?</p>
                <p class="learn-more-text">
                  Head to
                  <a href="https://bluecrew.com.au/" class="text-link">https://bluecrew.com.au/</a>
                </p>
                <p class="learn-more-text mb-0">
                  and
                  <a href="https://www.oceanyouth.org/" class="text-link"
                    >https://www.oceanyouth.org/</a
                  >
                </p>
              </div>
            </div>

            <!-- Game Grid -->
            <div class="game-grid desktop-game-grid">
              <div class="mobile-grid-container">
                <div class="grid-content">
                  <div class="grid-row" v-for="row in 4" :key="`row-${row}`">
                    <div v-for="col in 4" :key="`tile-${row}-${col}`" class="tile-wrapper">
                      <BingoTile
                        v-bind="challengeInfos[(row - 1) * 4 + (col - 1)]"
                        :selected="selectedTile === (row - 1) * 4 + (col - 1)"
                        :isBingo="
                          bingoRows[row - 1] ||
                          bingoCols[col - 1] ||
                          (row === col && bingoDiagonal[0]) ||
                          (row + col === 5 && bingoDiagonal[1])
                        "
                        @click="handleTileClick((row - 1) * 4 + (col - 1))"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>

      <!-- Mobile Layout -->
      <template v-else>
        <div class="mobile-content">
          <!-- Title Section -->
          <div class="header-section mobile-header">
            <h1 class="blingo-title text-primaryBlue">Blingo</h1>
            <h2 class="blingo-subtitle text-primaryGreen">Connecting to the ocean</h2>
          </div>

          <!-- Game Grid -->
          <div class="mobile-game-container">
            <div class="mobile-grid-container">
              <div class="grid-content">
                <div class="grid-row" v-for="row in 4" :key="`row-${row}`">
                  <div v-for="col in 4" :key="`tile-${row}-${col}`" class="tile-wrapper">
                    <BingoTile
                      v-bind="challengeInfos[(row - 1) * 4 + (col - 1)]"
                      :selected="selectedTile === (row - 1) * 4 + (col - 1)"
                      :isBingo="
                        bingoRows[row - 1] ||
                        bingoCols[col - 1] ||
                        (row === col && bingoDiagonal[0]) ||
                        (row + col === 5 && bingoDiagonal[1])
                      "
                      @click="handleTileClick((row - 1) * 4 + (col - 1))"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Challenge Card -->
        <div v-if="showChallengeCard" class="challenge-card-overlay">
          <ChallengeCard
            v-bind="currentChallenge"
            :is-logged-in="userStore.isLoggedIn"
            @close="handleCloseChallenge"
            @status-change="handleStatusChange"
          />
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
/* Bingo Glow */
.bingo-glow {
  animation: bingo-glow 1s infinite alternate;
}

@keyframes bingo-glow {
  0% {
    box-shadow: 0 0 10px rgba(255, 223, 0, 0.5);
  }
  100% {
    box-shadow: 0 0 20px rgba(255, 223, 0, 1);
  }
}

/* Main container */
.main-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Content wrapper */
.content-wrapper {
  width: 100%;
  max-width: 1200px;
  padding: 1rem;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  flex: 1;
}

/* Desktop styles */
.content-container {
  display: flex;
  justify-content: center;
  gap: 2rem;
  width: 100%;
}

.desktop-layout {
  width: 100%;
  display: flex;
  justify-content: center;
}

.left-section {
  flex: 0 0 500px;
  display: flex;
  flex-direction: column;
}

.desktop-game-grid {
  flex: 0 0 450px;
}

/* Mobile styles */
.mobile-content {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 0.5rem;
}

.mobile-game-container {
  padding: 0.25rem 0;
}

/* Header styles */
.header-section {
  width: 100%;
  margin-bottom: 0.5rem;
}

.blingo-title {
  font-family: 'Lilita One', cursive;
  text-align: center;
  margin-bottom: 0;
}

.blingo-subtitle {
  text-align: center;
  margin-top: 0;
}

/* Grid styles */
.mobile-grid-container {
  width: 100%;
  display: flex;
  justify-content: center;
}

.grid-content {
  display: inline-block;
  transform-origin: center;
}

.grid-row {
  display: flex;
  justify-content: center;
  margin: 0;
  padding: 0;
  line-height: 0;
}

.tile-wrapper {
  margin: 0;
  padding: 0;
  line-height: 0;
  font-size: 0;
}

/* Text styles */
.mobile-container .blingo-title {
  font-size: 2.5rem;
}

.mobile-container .blingo-subtitle {
  font-size: 1.25rem;
}

.desktop-header .blingo-title {
  font-size: 3rem;
}

.desktop-header .blingo-subtitle {
  font-size: 1.5rem;
}

/* Challenge card styles */
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

.desktop-challenge-card {
  width: 100%;
  margin: 0 auto 1rem;
  position: relative;
  z-index: 2;
}

/* Learn more section styles */
.learn-more-section {
  text-align: center;
  margin: 0;
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

.learn-more-text.mb-0 {
  margin-bottom: 0;
}

/* Responsive styles */
@media (max-width: 1200px) {
  .content-container {
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .left-section,
  .desktop-game-grid {
    width: 100%;
    max-width: 500px;
  }
}

@media (max-width: 480px) {
  .content-wrapper {
    padding: 0.5rem;
  }

  .grid-content {
    transform: scale(0.8);
  }

  .mobile-game-container {
    padding: 0.25rem 0;
  }
}

@media (max-width: 400px) {
  .content-wrapper {
    padding: 0.25rem;
  }

  .grid-content {
    transform: scale(0.7);
  }

  .mobile-game-container {
    padding: 0.25rem 0;
  }
}

@media (max-width: 350px) {
  .grid-content {
    transform: scale(0.65);
  }
}

@media (max-width: 300px) {
  .grid-content {
    transform: scale(0.6);
  }
}
</style>
