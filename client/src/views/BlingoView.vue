<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useDisplay } from 'vuetify'
import { useUserStore } from '@/stores/user'
import type { ChallengeInfo, ChallengeInfoAPI } from '@/types/challenge'
import BingoTile from '@/components/BingoTile.vue'
import ChallengeCard from '@/components/ChallengeCard.vue'
import WaveBanner from '@/components/WaveBanner.vue'
import server from '@/utils/server'
import { useMessageStore } from '@/stores/message'
import type { BingoData, BingoType } from '@/types/bingo'

const { mdAndDown } = useDisplay()
const userStore = useUserStore()
const gridSize = 4
const isLoading = ref(true)

const challengeInfos = ref<ChallengeInfo[]>([])
const messageStore = useMessageStore()

const fetchBingoGrid = async () => {
  isLoading.value = true
  server
    .get('/bingo-grid/')
    .then((res) => {
      challengeInfos.value = res.data.challenges.map((item: ChallengeInfoAPI): ChallengeInfo => {
        const chal = {
          title: item.name,
          points: item.points,
          type: item.challenge_type,
          description: item.description,
          status: userStore.isLoggedIn ? item.status : 'not started',
        }
        return chal
      })
      isLoading.value = false
    })
    .catch(() => {
      messageStore.showMessage('Error', 'Unexpected occured while fetching challenges.', 'error')
    })
}

const explodingLocations = ref<boolean[]>(Array(gridSize * gridSize).fill(false))
const bingoLocations = ref<boolean[]>(Array(gridSize * gridSize).fill(false))

const animateBingo = async (bingoType: BingoType, index?: number) => {
  return new Promise<void>((resolve) => {
    switch (bingoType) {
      case 'row':
        if (index !== undefined) {
          for (let i = 0; i < gridSize; i++) {
            bingoLocations.value[4 * index + i] = true
          }
        }
        break
      case 'column':
        if (index !== undefined) {
          for (let i = 0; i < gridSize; i++) {
            bingoLocations.value[index + 4 * i] = true
          }
        }
        break
      case 'diagonal':
        if (index !== undefined) {
          for (let i = 0; i < gridSize; i++) {
            bingoLocations.value[index + (index === 0 ? 5 : 3) * i] = true
          }
        }
        break
      case 'full':
        bingoLocations.value = Array(gridSize * gridSize).fill(true)
        break
    }

    console.log('🔥 Bingo Highlight Triggered:', bingoType, index)
    setTimeout(() => {
      bingoLocations.value = Array(gridSize * gridSize).fill(false)
      // we need to wait a short additional bit of time to ensure that certain indices
      // of bingoLocations.value don't get immediately toggled back, which would mean
      // that the animation would never be restarted
      setTimeout(() => resolve(), 200)
    }, 1000)
  })
}

const animateTileCompletion = (tileIndex: number) => {
  return new Promise<void>((resolve) => {
    explodingLocations.value[tileIndex] = true
    setTimeout(() => {
      explodingLocations.value[tileIndex] = false
      resolve()
    }, 1500)
  })
}

const selectedTile = ref<number | null>(null)
const showChallengeCard = ref(false)

const handleTileClick = (index: number) => {
  selectedTile.value = index
  showChallengeCard.value = true
}

const handleCloseChallenge = () => {
  showChallengeCard.value = false
  selectedTile.value = null
}

const handleStatusChange = async (
  status: 'not started' | 'started' | 'completed',
  bingoData: BingoData | undefined,
) => {
  if (selectedTile.value !== null) {
    challengeInfos.value[selectedTile.value].status = status
    if (status === 'completed') {
      const tileIndex = selectedTile.value
      // if a challenge is completed, close the challenge card so that the animations can be seen
      showChallengeCard.value = false
      selectedTile.value = null
      // animation tile completion
      await animateTileCompletion(tileIndex)
      // now animate any bingos
      if (bingoData) {
        if (bingoData.bingo_row !== -1) {
          await animateBingo('row', bingoData.bingo_row)
        }
        if (bingoData.bingo_col !== -1) {
          await animateBingo('column', bingoData.bingo_col)
        }
        if (bingoData.bingo_diag !== -1) {
          await animateBingo('diagonal', bingoData.bingo_diag)
        }
        if (bingoData.full_bingo) {
          await animateBingo('full')
        }
      }
    }
  }
}

async function temp() {
  await animateBingo('column', 1)
  await animateBingo('row', 0)
  await animateBingo('diagonal', 3)
  await animateBingo('full')
}

onMounted(() => {
  fetchBingoGrid()
})
</script>

<template>
  <WaveBanner imageSrc="/homepage-scaled.jpg" />
  <v-btn @click="temp">temp</v-btn>
  <v-container :class="{ vertical: mdAndDown }">
    <v-row>
      <v-col lg="5" cols="12">
        <div class="mb-8">
          <h1 class="blingo-title text-primaryBlue text-center">Blingo</h1>
          <h2 class="blingo-subtitle text-center text-primaryGreen">Connecting to the ocean</h2>
        </div>

        <!-- Challenge Card -->
        <component
          :is="mdAndDown ? 'v-dialog' : 'div'"
          v-model="showChallengeCard"
          v-if="showChallengeCard && selectedTile !== null"
          transition="dialog-bottom-transition"
        >
          <ChallengeCard
            v-bind="challengeInfos[selectedTile]"
            :position="selectedTile"
            :is-logged-in="userStore.isLoggedIn"
            @close="handleCloseChallenge"
            @status-change="handleStatusChange"
          />
        </component>

        <!-- Learn More Section (Only for Desktop) -->
        <div class="text-center text-primaryGreen mt-8" v-if="!mdAndDown">
          <p class="learn-more-title">Want to learn more?</p>
          <p class="learn-more-text">
            Head to
            <a href="https://bluecrew.com.au/" class="text-link">https://bluecrew.com.au/</a>
          </p>
          <p class="learn-more-text mb-0">
            and
            <a href="https://www.oceanyouth.org/" class="text-link">https://www.oceanyouth.org/</a>
          </p>
        </div>
      </v-col>

      <!-- Game Grid -->
      <v-col lg="7" cols="12" align="center">
        <div v-if="isLoading" class="text-center pa-4">
          <v-progress-circular indeterminate color="primaryBlue" />
        </div>

        <template v-else>
          <div class="grid-content">
            <div class="reward-text">
              <p>Challenge Complete!</p>
              <p>+100 points</p>
            </div>
            <div class="d-flex justify-center" v-for="row in 4" :key="`row-${row}`">
              <BingoTile
                v-for="col in 4"
                :key="`tile-${row}-${col}`"
                v-bind="challengeInfos[(row - 1) * 4 + (col - 1)]"
                :selected="selectedTile === (row - 1) * 4 + (col - 1)"
                :is-exploding="explodingLocations[(row - 1) * 4 + (col - 1)]"
                :isInBingo="bingoLocations[(row - 1) * 4 + (col - 1)]"
                @click="handleTileClick((row - 1) * 4 + (col - 1))"
              />
            </div>
          </div>
        </template>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.blingo-title {
  font-family: 'Lilita One', cursive;
}

/* Grid styles */
.grid-content {
  width: 100%;
  display: inline-block;
  transform-origin: center;
  position: relative;
}

.blingo-title {
  font-size: 3rem;
}

.blingo-subtitle {
  font-size: 1.5rem;
}

.vertical .blingo-title {
  font-size: 2.5rem;
}

.vertical .blingo-subtitle {
  font-size: 1.25rem;
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

.reward-text {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translateX(-50%) translateY(-50%);
  color: #009d00;
  font-size: 20px;
  font-weight: semibold;
  font-family: Lilita One;
  text-shadow: 1px 1px 2px black;
  z-index: 2000;
}
</style>
