<script setup lang="ts">
defineProps<{
  rank: number
  avatarIndex: number
  name: string
  points: number
  isHighlighted: boolean
}>()
</script>

<template>
  <div
    :class="[isHighlighted ? 'bg-primaryPink' : 'bg-creamWhite text-primaryGrey']"
    class="leaderboard-row"
  >
    <p class="font-weight-bold">{{ rank }}</p>
    <v-img
      class="rounded-circle"
      max-height="32"
      max-width="32"
      min-width="32"
      cover
      src="https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg"
    ></v-img>
    <p class="me-auto font-weight-bold truncate-name">{{ name }}</p>
    <p :class="[isHighlighted ? 'font-weight-bold' : '']" class="text-right points">
      {{ points }} pts
    </p>
  </div>
</template>

<style scoped>
.leaderboard-row {
  display: flex;
  gap: 16px;
  min-height: 50px;
  padding-left: 20px;
  padding-right: 20px;
  align-items: center;
  border-radius: 8px;
  color: rgb(var(--v-theme-primaryGrey));
}

.truncate-name {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.points {
  white-space: nowrap;
}
</style>
