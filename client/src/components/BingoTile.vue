<script setup lang="ts">
import { computed } from 'vue'
import type { ChallengeType, ChallengeStatus } from '@/types/challenge'

const props = defineProps<{
  type: ChallengeType
  title: string
  status: ChallengeStatus
  selected: boolean
}>()

const icon = computed(() => {
  switch (props.type) {
    case 'act':
      return 'walking.svg'
    case 'understand':
      return 'brain.svg'
    default:
      return 'link.svg'
  }
})

const backgroundColour = computed(() => {
  switch (props.status) {
    case 'started':
      return 'bg-primaryPink'
    case 'completed':
      return 'bg-lightBlue'
    default:
      return 'bg-creamWhite'
  }
})

const textColour = computed(() => {
  switch (props.status) {
    case 'completed':
      return 'text-primaryWhite'
    default:
      return 'text-primaryBlack'
  }
})

const iconBackground = computed(() => {
  switch (backgroundColour.value) {
    case 'bg-creamWhite':
      return 'dark'
    default:
      return 'light'
  }
})
</script>

<template>
  <div
    :class="[backgroundColour, textColour, selected ? 'border-selected' : 'border-subtle']"
    class="outer-tile rounded-lg d-flex flex-column align-center cursor-pointer w-100"
  >
    <v-img class="icon" :class="iconBackground" :src="icon" />
    <p class="w-100 tile-text text-center font-weight-bold overflow-x-hidden overflow-hidden">
      {{ title }}
    </p>
  </div>
</template>

<style scoped>
.outer-tile {
  padding-bottom: 0.2rem;
  aspect-ratio: 1 / 1;
  padding: 0.5rem;
}

.border-subtle {
  border: #4f4f4f 0.05rem solid;
}

.border-selected {
  border: #4f4f4f 0.15rem solid;
  box-shadow: 0.1rem 0.1rem 0.2rem 0.1rem #4f4f4f;
}

.tile-text {
  font-size: 0.6rem;
  line-height: 1.2;
}

.icon {
  width: 40%;
  height: 70%;
}

.icon.light {
  filter: invert();
}

.icon.dark {
  filter: contrast(100%) brightness(0%);
}
</style>
