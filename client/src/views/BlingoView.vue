<script setup lang="ts">
import { ref, computed } from 'vue'
import { useDisplay } from 'vuetify'
import BlingoTile from '@/components/BingoTile.vue'
import ChallengeCard from '@/components/ChallengeCard.vue'
import WaveBanner from '@/components/WaveBanner.vue'


const { xs } = useDisplay()

const containerClass = computed(() => (!xs.value ? 'desktop-container' : 'mobile-container'))

const selectedTile = ref<number | null>(null)
const showChallengeCard = ref(false)
const currentChallenge = ref({
  title: 'Watch an Ocean Documentary',
  points: 200,
  type: 'understand' as const,
  description: 'Here are some of our top picks! You can choose one of them or watch one of your own. Tell us what you thought and submit a picture.',
  status: 'not started' as const,
})

const handleTileClick = (index: number) => {
  selectedTile.value = index
  showChallengeCard.value = true
}

const handleCloseChallenge = () => {
  showChallengeCard.value = false
  selectedTile.value = null
}

const handleStatusChange = (newStatus: 'not started' | 'started' | 'completed') => {
  currentChallenge.value.status = newStatus
}
</script>

<template>
  <WaveBanner imageSrc="/homepage-scaled.jpg" />

  <div :class="['content-wrapper', containerClass]">
    <!-- Desktop Version -->
    <template v-if="!xs">
      <div class="desktop-layout">

        <div class="left-section">

          <div class="header-section desktop-header">
            <h1 class="blingo-title">Blingo</h1>
            <h2 class="blingo-subtitle text-primaryGreen">Connecting to the ocean</h2>
          </div>

          <!-- Learn More Section -->
          <div class="learn-more-section">
            <p class="learn-more-title">Want to learn more?</p>
            <p class="learn-more-text">
              Head to <a href="https://bluecrew.com.au/" class="text-link">https://bluecrew.com.au/</a>
            </p>
            <p class="learn-more-text">
              and <a href="https://www.oceanyouth.org/" class="text-link">https://www.oceanyouth.org/</a>
            </p>
          </div>
        </div>

        <!-- Game Grid -->
        <div class="game-grid">
          <div class="grid-row" v-for="row in 4" :key="`row-${row}`">
            <BlingoTile
              v-for="(_, col) in 4"
              :key="`tile-${row}-${col}`"
              type="connect"
              text="placeholder text"
              status="not started"
              :selected="selectedTile === (row - 1) * 4 + col"
              @click="handleTileClick((row - 1) * 4 + col)"
            />
          </div>
        </div>
      </div>
    </template>

    <!-- Mobile Layout -->
    <template v-else>
      <!-- Title Section -->
      <div class="header-section mobile-header">
        <h1 class="blingo-title">Blingo</h1>
        <h2 class="blingo-subtitle text-priamryGreen">Connecting to the ocean</h2>
      </div>

      <!-- Game Grid -->
      <div class="game-grid">
        <div class="grid-row" v-for="row in 4" :key="`row-${row}`">
          <BlingoTile
            v-for="(_, col) in 4"
            :key="`tile-${row}-${col}`"
            type="connect"
            text="placeholder text"
            status="not started"
            :selected="selectedTile === (row - 1) * 4 + col"
            @click="handleTileClick((row - 1) * 4 + col)"
          />
        </div>
      </div>

      <!-- Learn More Section -->
      <div class="learn-more-section">
        <p class="learn-more-title">Want to learn more?</p>
        <p class="learn-more-text">
          Head to <a href="https://bluecrew.com.au/" class="text-link">https://bluecrew.com.au/</a>
        </p>
        <p class="learn-more-text">
          and <a href="https://www.oceanyouth.org/" class="text-link">https://www.oceanyouth.org/</a>
        </p>
      </div>
    </template>

    <!-- Challenge Card -->
    <div v-if="showChallengeCard" class="challenge-card-overlay">
      <ChallengeCard
        v-bind="currentChallenge"
        :is-logged-in="true"
        @close="handleCloseChallenge"
        @status-change="handleStatusChange"
      />
    </div>
  </div>
</template>

<style scoped>
.content-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  padding: 1.25rem;
}

.header-section {
  margin-bottom: 1.5rem;
}

.blingo-title {
  font-size: 2.5rem;
  font-weight: bold;
  text-align: center;
}

.blingo-subtitle {
  font-size: 1.25rem;
  text-align: center;
}


.desktop-header {
  text-align: left;
}

.desktop-header .blingo-title,
.desktop-header .blingo-subtitle {
  text-align: center;
}

.learn-more-section {
  text-align: center;
}

.learn-more-title {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.learn-more-text {
  margin: 0.5rem 0;
}

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

.mobile-container {
  flex-direction: column;
  padding: 1.25rem;
}

.mobile-container .learn-more-section {
  text-align: center;
}

.desktop-layout {
  display: flex;
  justify-content: space-between;
  width: 100%;
  padding: 2rem;
}

.left-section {
  flex: 1;
  max-width: 30%;
}

.game-grid {
  flex: 2;
  display: flex;
  flex-direction: column;
}

.grid-row {
  display: flex;
  gap: 0.25rem;
  margin-bottom: 0.25rem;
}
.challenge-card-overlay {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>
