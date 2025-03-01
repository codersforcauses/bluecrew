<script setup lang="ts">
import { computed } from 'vue'
import type { BingoTileProps } from '@/types/bingo'

const props = defineProps<BingoTileProps>()

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
      return 'bg-primaryGreen-unimportant'
    case 'completed':
      return 'bg-lightBlue-unimportant'
    default:
      return 'bg-creamWhite-unimportant'
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
    case 'bg-creamWhite-unimportant':
      return 'dark'
    default:
      return 'light'
  }
})
</script>

<template>
  <div
    :class="[
      textColour,
      backgroundColour,
      interactionAllowed ? 'cursor-pointer' : 'cursor-not-allowed',
      selected ? 'border-selected' : 'border-subtle',
      isInBingo ? 'bingo-highlight' : '',
      isExploding ? 'explode-animation' : '',
    ]"
    class="outer-tile rounded-lg d-flex flex-column align-center cursor-pointer"
    :title="title"
  >
    <v-img class="icon" :class="iconBackground" :src="icon" />
    <p class="tile-text text-center font-weight-bold">{{ title }}</p>
  </div>
</template>

<style scoped>
.explode-animation {
  z-index: 1000;
  transform-origin: center;
  animation: explode 1s ease-out 0.2s;
}

@keyframes explode {
  from {
    transform: scale(1);
    opacity: 1;
  }

  to {
    transform: scale(2);
    opacity: 0;
  }
}

/* defining these classes so that they can be overriden in an animation */
.bg-primaryGreen-unimportant {
  background-color: rgb(var(--v-theme-primaryGreen));
}

.bg-lightBlue-unimportant {
  background-color: rgb(var(--v-theme-lightBlue));
}

.bg-creamWhite-unimportant {
  background-color: rgb(var(--v-theme-creamWhite));
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
  overflow: hidden;
}

.bingo-highlight {
  animation: bingo-flash 1.5s ease-in-out;
}

@keyframes bingo-flash {
  0%,
  100% {
    background-color: rgb(var(--v-theme-lightBlue));
  }

  50% {
    background-color: #3fe0d5;
  }
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

@media (max-width: 500px) {
  .outer-tile {
    width: 100px;
    height: 100px;
    min-width: 100px;
    min-height: 100px;
    padding: 0.3rem;
  }

  .tile-text {
    font-size: 0.6rem;
    margin-top: 0.3rem;
  }
}

@media (max-width: 400px) {
  .outer-tile {
    width: 80px;
    height: 80px;
    min-width: 80px;
    min-height: 80px;
    padding: 0.2rem;
  }

  .tile-text {
    font-size: 0.5rem;
    margin-top: 0.2rem;
  }
}
</style>
