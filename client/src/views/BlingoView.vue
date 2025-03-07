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
import type { ExtendedAxiosError } from '@/types/other'

const { mdAndDown } = useDisplay()
const userStore = useUserStore()
const gridSize = 4
const isLoading = ref(true)
const challengeInfos = ref<ChallengeInfo[]>([])
const messageStore = useMessageStore()
const tileInteractionsOff = ref<boolean>(false)

const explodingLocations = ref<boolean[]>(Array(gridSize * gridSize).fill(false))
const bingoLocations = ref<boolean[]>(Array(gridSize * gridSize).fill(false))
const showReward = ref<boolean>(false)
const rewardText = ref<string>('')
const rewardPoints = ref<number>(0)

const explosionAnimationLength = 2000
const bingoAnimationLength = 1500
const rewardAnimationEntryLength = 2000
const rewardAnimationLeaveLength = 800

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
    .catch((error: ExtendedAxiosError) => {
      messageStore.handleUnexpectedError(error.config?.session_expired, false)
    })
}

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

    setTimeout(() => {
      bingoLocations.value = Array(gridSize * gridSize).fill(false)
      // we need to wait a short additional bit of time to ensure that certain indices
      // of bingoLocations.value don't get immediately toggled back, which would mean
      // that the animation would never be restarted
      setTimeout(() => resolve(), 200)
    }, bingoAnimationLength)
  })
}

const animateTileCompletion = (tileIndex: number) => {
  return new Promise<void>((resolve) => {
    explodingLocations.value[tileIndex] = true
    setTimeout(() => {
      explodingLocations.value[tileIndex] = false
      resolve()
    }, explosionAnimationLength)
  })
}

const animateRewardText = (text: string, points: number) => {
  return new Promise<void>((resolve) => {
    rewardText.value = text
    rewardPoints.value = points
    showReward.value = true
    setTimeout(() => {
      showReward.value = false
      setTimeout(() => resolve(), rewardAnimationLeaveLength)
    }, rewardAnimationEntryLength)
  })
}

const selectedTile = ref<number | null>(null)
const showChallengeCard = ref(false)

const handleTileClick = (index: number) => {
  if (!tileInteractionsOff.value) {
    selectedTile.value = index
    showChallengeCard.value = true
  }
}

const handleCloseChallenge = () => {
  showChallengeCard.value = false
  selectedTile.value = null
}

const handleStart = (index: number) => {
  challengeInfos.value[index].status = 'started'
}

const handleComplete = async (bingoData: BingoData, index: number) => {
  challengeInfos.value[index].status = 'completed'
  // if a challenge is completed, close the challenge card so that the animations can be seen
  showChallengeCard.value = false
  selectedTile.value = null
  tileInteractionsOff.value = true
  // animation tile completion
  await Promise.all([
    animateTileCompletion(index),
    animateRewardText('Challenge Completed!', bingoData.challenge_points),
  ])
  // now animate any bingos
  if (bingoData.bingo_points > 0) {
    rewardText.value = 'Bingo!'
    rewardPoints.value = bingoData.bingo_points
    showReward.value = true
    const bingoAnimationPromises = async () => {
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
    await Promise.all([
      bingoAnimationPromises(),
      animateRewardText('Bingo!', bingoData.bingo_points),
    ])
    tileInteractionsOff.value = false
  }
}

onMounted(() => {
  fetchBingoGrid()
})
</script>

<template>
  <WaveBanner imageSrc="/homepage-scaled.jpg" altText="Top view of people building sandcastles" />
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
            @start="handleStart"
            @complete="handleComplete"
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
            <Transition name="show-reward">
              <div v-show="showReward" class="reward-text">
                <p>{{ rewardText }}</p>
                <p>+{{ rewardPoints }} points</p>
              </div>
            </Transition>
            <div class="d-flex justify-center" v-for="row in 4" :key="`row-${row}`">
              <BingoTile
                v-for="col in 4"
                :key="`tile-${row}-${col}`"
                v-bind="challengeInfos[(row - 1) * 4 + (col - 1)]"
                :selected="selectedTile === (row - 1) * 4 + (col - 1)"
                :is-exploding="explodingLocations[(row - 1) * 4 + (col - 1)]"
                :isInBingo="bingoLocations[(row - 1) * 4 + (col - 1)]"
                @click="handleTileClick((row - 1) * 4 + (col - 1))"
                :interaction-allowed="!tileInteractionsOff"
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
  width: 100%;
  top: 50%;
  scale: 1;
  transform: translateY(-50%);
  transform-origin: top center;
  color: #ffffff;
  font-size: 30px;
  font-weight: semibold;
  font-family: Lilita One;
  text-shadow: 0px 0px 10px black;
  z-index: 2000;
}

.show-reward-enter-active {
  display: block;
  animation: show-reward 1.5s ease forwards;
}

.show-reward-leave-active {
  display: block;
  animation: show-reward 0.5s ease reverse;
}

@keyframes show-reward {
  from {
    scale: 0;
  }

  to {
    scale: 1;
  }
}

@media (max-width: 600px) {
  .reward-text {
    font-size: 24px;
  }
}
</style>
