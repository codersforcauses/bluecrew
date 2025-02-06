<script setup lang="ts">
import WaveBanner from '@/components/WaveBanner.vue'
import { useMessageStore } from '@/stores/message';
import server from '@/utils/server';
import { ref } from 'vue';

const messageStore = useMessageStore()
const isInt = (val: string) => /^[1-9]\d*$/.test(val) || "Please enter a whole number"
const challengeIds = ref<string[]>(new Array(16).fill(""))

function updateBingo() {
  const intArray = challengeIds.value.map(s => parseInt(s))
  console.log(intArray)
  server.post("update-bingo-grid/", { challenges: intArray }).then(() => {
    messageStore.showMessage("Success", "A new bingo grid has gone live with the challenges you specified", "success")
  }).catch((error) => {
    console.log(error)
  })
}
</script>

<template>
  <WaveBanner image-src="teambuilding-background.jpg" />
  <h2 class="text-center text-primaryBlue mb-4">Admin</h2>
  <p class="text-primaryGreen text-center">Please enter the IDs of the challenges you'd like for a new bingo grid</p>
  <div class="d-flex flex-column align-center mt-5 px-5">
    <div v-for="row in 4" :key="row" class="d-flex flex-row ga-1 row mb-1">
      <v-text-field v-for="col in 4" :key="col" hide-details variant="outlined" bg-color="primaryBrown"
        v-model="challengeIds[4 * (row - 1) + col - 1]" :rules="[isInt]" />
    </div>
    <v-btn @click="updateBingo" class="my-4 bg-primaryGreen">Go Live!</v-btn>
  </div>
</template>

<style scoped>
.row {
  max-width: 400px;
}
</style>
