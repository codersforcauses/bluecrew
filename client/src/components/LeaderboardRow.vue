<script setup lang="ts">
import avatarPaths from '@/utils/avatar'
import { navigateToProfile } from '@/router'

defineProps<{
  rank: number
  avatarIndex: number
  name: string
  points: number
  isHighlighted: boolean
}>()

const handleUsernameClick = (username: string) => {
  navigateToProfile(username)
}
</script>

<template>
  <div
    :class="[isHighlighted ? 'bg-primaryGreen' : 'bg-creamWhite text-primaryGrey']"
    class="leaderboard-row"
  >
    <p class="font-weight-bold">{{ rank }}</p>
    <v-img
      class="rounded-circle"
      max-height="32"
      max-width="32"
      min-width="32"
      cover
      :src="`/${avatarPaths[avatarIndex]}`"
    />
    <p
      class="me-auto font-weight-bold truncate-name username-link"
      @click="handleUsernameClick(name)"
    >
      {{ name }}
    </p>
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

.username-link {
  cursor: pointer;

  &:hover {
    text-decoration: underline;
    color: rgb(var(--v-theme-primaryBlue));
  }
}
</style>
