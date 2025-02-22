<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { ChallengeType, ChallengeStatus } from '@/types/challenge'

const props = defineProps<{
  type: ChallengeType
  title: string
  status: ChallengeStatus
  selected: boolean
  isBingo: boolean
}>()

const isExploding = ref(false)

watch(
  () => props.status,
  (newStatus) => {
    if (newStatus === 'completed') {
      isExploding.value = true
      setTimeout(() => {
        isExploding.value = false
      }, 500)
    }
  },
)

// Compute icon based on challenge type
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
      return 'bg-primaryGreen'
    case 'completed':
      return 'bg-lightBlue'
    default:
      return 'bg-creamWhite'
  }
})

// Compute text color based on status
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
  <transition name="explode">
    <div
      v-if="!isExploding"
      :class="[
        backgroundColour,
        textColour,
        selected ? 'border-selected' : 'border-subtle',
        isBingo ? 'bingo-highlight' : '',
      ]"
      class="outer-tile rounded-lg d-flex flex-column align-center cursor-pointer"
      :title="title"
    >
      <v-img class="icon" :class="iconBackground" :src="icon" />
      <p class="tile-text text-center font-weight-bold">{{ title }}</p>
    </div>
  </transition>
</template>

<style scoped>
.explode-enter-active {
  animation: explode 0.5s ease-out forwards;
}

@keyframes explode {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.5);
    opacity: 0.5;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}

.bingo-highlight {
  box-shadow: 0 0 15px 6px rgba(0, 255, 255, 0.6);
  border: 2px solid rgba(0, 255, 255, 0.8);
}

.outer-tile {
  padding: 0.5rem;
  width: 150px;
  height: 150px;
  min-width: 150px;
  min-height: 150px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
}

.border-subtle {
  border: #4f4f4f 0.05rem solid;
}

.border-selected {
  border: #4f4f4f 0.15rem solid;
  box-shadow: 0.1rem 0.1rem 0.2rem 0.1rem #4f4f4f;
}

.tile-text {
  font-size: 0.9rem;
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
  padding: 0 0.25rem;
  margin-top: 0.5rem;
}

.outer-tile:hover {
  z-index: 1;
}

.icon {
  width: 40%;
  height: 40%;
  object-fit: contain;
  margin-bottom: 0.5rem;
}

.icon.light {
  filter: invert();
}
.icon.dark {
  filter: contrast(100%) brightness(0%);
}

@media (max-width: 600px) {
  .outer-tile {
    width: 120px;
    height: 120px;
    min-width: 120px;
    min-height: 120px;
    padding: 0.4rem;
  }

  .tile-text {
    font-size: 0.75rem;
    margin-top: 0.4rem;
  }

  .icon {
    width: 35%;
    height: 35%;
    margin-bottom: 0.4rem;
  }
}
</style>
