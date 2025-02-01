<script setup lang="ts">
import { ref } from 'vue'
import BlingoTile from '@/components/BingoTile.vue'
import ChallengeCard from '@/components/ChallengeCard.vue'

// State management
const selectedTile = ref<number | null>(null)
const showChallengeCard = ref(false)
const currentChallenge = ref({
  title: 'Watch an Ocean Documentary',
  points: 200,
  type: 'understand' as const,
  description: 'Here are some of our top picks! You can choose one of them or watch one of your own. Tell us what you thought and submit a picture.',
  status: 'not started' as const
})

// Handle tile click event
const handleTileClick = (index: number) => {
  selectedTile.value = index
  showChallengeCard.value = true
}

// Handle challenge card close
const handleCloseChallenge = () => {
  showChallengeCard.value = false
  selectedTile.value = null
}

// Handle status change
const handleStatusChange = (newStatus: 'not started' | 'started' | 'completed') => {
  currentChallenge.value.status = newStatus
}
</script>

<template>
  <div class="content-wrapper">
    <!-- Title Section -->
    <div class="header-section">
      <h1 class="text-primaryBlack blingo-title text-center">Blingo</h1>
      <h2 class="text-lightBlue blingo-subtitle text-center">Connecting to the ocean</h2>
    </div>

    <!-- Game Grid -->
    <div class="game-grid">
      <div class="grid-row">
        <BlingoTile v-for="(_, index) in 4" :key="`row1-${index}`" type="connect" text="placeholder text"
          status="not started" :selected="selectedTile === index" @click="handleTileClick(index)" />
      </div>
      <div class="grid-row">
        <BlingoTile v-for="(_, index) in 4" :key="`row2-${index}`" type="connect" text="placeholder text"
          status="not started" :selected="selectedTile === index + 4" @click="handleTileClick(index + 4)" />
      </div>
      <div class="grid-row">
        <BlingoTile v-for="(_, index) in 4" :key="`row3-${index}`" type="act" text="placeholder text"
          status="not started" :selected="selectedTile === index + 8" @click="handleTileClick(index + 8)" />
      </div>
      <div class="grid-row">
        <BlingoTile v-for="(_, index) in 4" :key="`row4-${index}`" type="understand" text="placeholder text"
          status="not started" :selected="selectedTile === index + 12" @click="handleTileClick(index + 12)" />
      </div>
    </div>

    <!-- Learn More Section -->
    <div class="learn-more-section">
      <p class="text-primaryBlack learn-more-title font-weight-medium">Want to learn more?</p>
      <p class="learn-more-text">
        Head to <a href="https://bluecrew.com.au/"
          class="text-lightBlue text-decoration-none">https://bluecrew.com.au/</a>
      </p>
      <p class="learn-more-text mb-0">
        and <a href="https://www.oceanyouth.org/"
          class="text-lightBlue text-decoration-none">https://www.oceanyouth.org/</a>
      </p>
    </div>

    <!-- Challenge Card Modal -->
    <div v-if="showChallengeCard" class="challenge-card-overlay">
      <ChallengeCard v-bind="currentChallenge" :is-logged-in="true" @close="handleCloseChallenge"
        @status-change="handleStatusChange" />
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
  text-align: center;
  margin-bottom: 2rem;
}

.blingo-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  line-height: 1.2;
}

.blingo-subtitle {
  font-size: 1.25rem;
  line-height: 1.4;
}

.game-grid {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto 2rem;
}

.grid-row {
  display: flex;
  gap: 0.25rem;
  margin-bottom: 0.25rem;
}

.grid-row:last-child {
  margin-bottom: 0;
}

.learn-more-section {
  text-align: center;
}

.learn-more-title {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.learn-more-text {
  margin: 0.25rem 0;
  font-size: 1rem;
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

/* Desktop styles */
@media (min-width: 1024px) {
  .content-wrapper {
    padding: 2rem;
  }

  .game-grid {
    width: 80%;
    margin: 0 auto 3rem;
  }

  .grid-row {
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .blingo-title {
    font-size: 3rem;
  }

  .blingo-subtitle {
    font-size: 1.5rem;
  }
}

/* Mobile styles */
@media (max-width: 1023px) {
  .content-wrapper {
    padding: 1.25rem;
  }

  .game-grid {
    width: 100%;
  }
}
</style>