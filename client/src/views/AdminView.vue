<script setup lang="ts">
import WaveBanner from '@/components/WaveBanner.vue'
import { useMessageStore } from '@/stores/message'
import type { ExtendedAxiosError } from '@/types/other'
import server from '@/utils/server'
import { ref } from 'vue'

const isValid = ref(false)
const errorMessage = ref('')
const messageStore = useMessageStore()
const required = (value: string) => !!value || 'Required.'
const isInt = (val: string) =>
  val.length === 0 || /^[1-9]\d*$/.test(val) || 'Please enter a whole number'
const initialContents = new Array(16).fill('')
const challengeIds = ref<string[]>([...initialContents])

function extractInvalidId(errorMessage: string): number | undefined {
  const startIndex = errorMessage.indexOf('Invalid pk')
  if (startIndex === -1) {
    return undefined
  }
  const endIndex = errorMessage.indexOf(' - object does not exist.')
  return parseInt(errorMessage.slice(startIndex + 12, endIndex - 1))
}

function updateBingo() {
  if (!isValid.value) {
    messageStore.showMessage(
      'Warning',
      'Please enter a valid challenge ID in each cell.',
      'warning',
    )
    return
  }
  const intArray = challengeIds.value.map((s) => parseInt(s))
  server
    .post('update-bingo-grid/', { challenges: intArray })
    .then(() => {
      messageStore.showMessage(
        'Success',
        'A new bingo grid has gone live with the challenges you specified',
        'success',
      )
      challengeIds.value = [...initialContents]
    })
    .catch((error: ExtendedAxiosError) => {
      const challenges = (error.response?.data as { challenges?: [string, ...string[]] })
        ?.challenges

      if (challenges) {
        const invalidId = extractInvalidId(challenges[0])
        errorMessage.value = invalidId
          ? `There does not exist a challenge with id ${invalidId}.`
          : challenges[0]
      } else {
        messageStore.handleUnexpectedError(error.config?.session_expired, false)
      }
    })
}
</script>

<template>
  <WaveBanner image-src="octopus-tentacles.png" altText="Bottom view of octopus tentacles" />
  <h2 class="text-center text-primaryBlue mb-4">Admin</h2>
  <p class="text-primaryGreen text-center">
    Please enter the IDs of the challenges you'd like for a new bingo grid
  </p>
  <v-form v-model="isValid" @submit.prevent="updateBingo" validate-on="invalid-input">
    <div class="d-flex flex-column align-center mt-5 px-5">
      <div v-for="row in 4" :key="row" class="d-flex flex-row ga-1 row mb-1">
        <v-text-field
          v-for="col in 4"
          :key="col"
          hide-details
          variant="outlined"
          bg-color="primaryBrown"
          v-model="challengeIds[4 * (row - 1) + col - 1]"
          :rules="[required, isInt]"
          @focus="errorMessage = ''"
        />
      </div>
      <p class="text-center text-red">{{ errorMessage }}</p>
      <v-btn type="submit" class="my-4 bg-primaryGreen">Go Live!</v-btn>
    </div>
  </v-form>
</template>

<style scoped>
.row {
  max-width: 400px;
}
</style>
