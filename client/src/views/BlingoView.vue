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

interface BingoData {
  bingo_rows: number[]
  bingo_cols: number[]
  bingo_diag: number[]
  full_bingo: boolean
}

interface BingoType {
  type: 'row' | 'column' | 'diagonal' | 'full'
  index?: number
}

const bingoRows = ref<boolean[]>(Array(gridSize).fill(false))
const bingoCols = ref<boolean[]>(Array(gridSize).fill(false))
const bingoDiagonal = ref<boolean[]>([false, false]) // [↘, ↙]

const handleBingoCompleted = (bingoData: BingoData) => {
  console.log('✅ Received Bingo Data:', bingoData)

  const bingo_rows = Array.isArray(bingoData.bingo_rows)
    ? bingoData.bingo_rows.filter((r) => r >= 0 && r < gridSize)
    : []
  const bingo_cols = Array.isArray(bingoData.bingo_cols)
    ? bingoData.bingo_cols.filter((c) => (c >= 0 && c < gridSize) || c === -1)
    : []
  const bingo_diag = Array.isArray(bingoData.bingo_diag)
    ? bingoData.bingo_diag.filter((d) => d === 0 || d === 3 || d === -1)
    : []
  const full_bingo = !!bingoData.full_bingo

  console.log('📊 Processed Bingo Data:', {
    Rows: bingo_rows,
    Columns: bingo_cols,
    Diagonal: bingo_diag,
    FullBingo: full_bingo,
  })

  const bingos: BingoType[] = []

  bingo_rows.forEach((row) => {
    if (row >= 0 && row < gridSize) {
      console.log(`📢 Row Bingo Achieved at Row ${row}`)
      bingos.push({ type: 'row', index: row } as BingoType)
    }
  })

  bingo_cols.forEach((col) => {
    if (col >= 0 && col < gridSize) {
      console.log(`📢 Column Bingo Achieved at Column ${col}`)
      bingos.push({ type: 'column', index: col } as BingoType)
    }
  })

  bingo_diag.forEach((diag) => {
    if (diag === 0 || diag === 3) {
      console.log(`📢 Diagonal Bingo Achieved at Index ${diag}`)
      bingos.push({ type: 'diagonal', index: diag } as BingoType)
    }
  })

  if (full_bingo) {
    console.log('🎉 Full Bingo Achieved!')
    bingos.push({ type: 'full' } as BingoType)
  }

  if (bingos.length > 0) {
    ;(async () => {
      for (const bingo of bingos) {
        await animateBingo(bingo)
      }
    })()
  } else {
    console.warn('⚠️ No Bingo Achieved! Stopping animation.')
  }
}

const animateBingo = async (bingo: BingoType) => {
  return new Promise<void>((resolve) => {
    switch (bingo.type) {
      case 'row':
        if (bingo.index !== undefined) {
          const updatedRows = [...bingoRows.value]
          updatedRows[bingo.index] = true
          bingoRows.value = updatedRows
        }
        break
      case 'column':
        if (bingo.index !== undefined) {
          const updatedCols = [...bingoCols.value]
          updatedCols[bingo.index] = true
          bingoCols.value = updatedCols
        }
        break
      case 'diagonal':
        if (bingo.index !== undefined) {
          const updatedDiag = [...bingoDiagonal.value]
          updatedDiag[bingo.index] = true
          bingoDiagonal.value = updatedDiag
        }
        break
      case 'full':
        bingoRows.value = Array(gridSize).fill(true)
        bingoCols.value = Array(gridSize).fill(true)
        bingoDiagonal.value = [true, true]
        break
    }

    console.log('🔥 Bingo Highlight Triggered:', bingo)

    setTimeout(() => {
      bingoRows.value = Array(gridSize).fill(false)
      bingoCols.value = Array(gridSize).fill(false)
      bingoDiagonal.value = [false, false]
      resolve()
    }, 1500)
  })
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
    console.log('Status changed')
    challengeInfos.value[selectedTile.value].status = newStatus
    currentChallenge.value.status = newStatus
  }
}

onMounted(() => {
  fetchBingoGrid()
})
</script>

<template>
  <WaveBanner imageSrc="/homepage-scaled.jpg" />
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
            v-bind="currentChallenge"
            :position="selectedTile"
            :is-logged-in="userStore.isLoggedIn"
            @close="handleCloseChallenge"
            @status-change="handleStatusChange"
            @bingoCompleted="handleBingoCompleted"
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
            <div class="d-flex justify-center" v-for="row in 4" :key="`row-${row}`">
              <BingoTile
                v-for="col in 4"
                :key="`tile-${row}-${col}`"
                v-bind="challengeInfos[(row - 1) * 4 + (col - 1)]"
                :selected="selectedTile === (row - 1) * 4 + (col - 1)"
                :isBingo="
                  bingoRows[row - 1] ||
                  bingoCols[col - 1] ||
                  (row === col && bingoDiagonal[0]) ||
                  (row + col === gridSize + 1 && !!bingoDiagonal[1])
                "
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
</style>
