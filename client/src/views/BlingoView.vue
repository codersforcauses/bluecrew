<script setup lang="ts">
import BlingoTile from '@/components/BingoTile.vue'
</script>

<template>
  <div class="d-flex flex-column align-center mt-5 mx-5">
    <div class="d-flex ga-1 w-100">
      <BlingoTile type="connect" text="placeholder text" status="not started" :selected="false" />
      <BlingoTile type="act" text="placeholder text" status="started" :selected="false" />
      <BlingoTile
        type="understand"
        text="placeholder text"
        status="not started"
        :selected="false"
      />
      <BlingoTile type="connect" text="placeholder text" status="completed" :selected="false" />
    </div>
    <div class="d-flex ga-1 mt-1 w-100">
      <BlingoTile type="connect" text="placeholder text" status="not started" :selected="false" />
      <BlingoTile
        type="understand"
        text="placeholder text"
        status="not started"
        :selected="false"
      />
      <BlingoTile type="act" text="placeholder text" status="completed" :selected="false" />
      <BlingoTile type="act" text="placeholder text" status="not started" :selected="false" />
    </div>
    <div class="d-flex ga-1 mt-1 w-100">
      <BlingoTile type="act" text="placeholder text" status="not started" :selected="false" />
      <BlingoTile type="connect" text="placeholder text" status="not started" :selected="true" />
      <BlingoTile
        type="understand"
        text="placeholder text"
        status="not started"
        :selected="false"
      />
      <BlingoTile type="connect" text="placeholder text" status="not started" :selected="false" />
    </div>
    <div class="d-flex ga-1 mt-1 w-100">
      <BlingoTile
        type="understand"
        text="placeholder text"
        status="not started"
        :selected="false"
      />
      <BlingoTile type="connect" text="placeholder text" status="not started" :selected="false" />
      <BlingoTile type="act" text="placeholder text" status="not started" :selected="false" />
      <BlingoTile
        type="understand"
        text="placeholder text"
        status="not started"
        :selected="false"
      />
    </div>
  </div>
</template>

<style scoped></style>

