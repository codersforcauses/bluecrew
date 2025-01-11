<script setup lang="ts">
import BlingoTile from '@/components/BingoTile.vue'
</script>

<template>
    <div class="d-flex ga-1">
        <BlingoTile type="connect" text="placeholder text" status="started" selected=True />
        <BlingoTile type="act" text="placeholder text" status="not started" selected="false" />
        <BlingoTile type="understand" text="placeholder text" status="not started" selected="true" />
        <BlingoTile type="connect" text="placeholder text" status="completed" selected="true" />
    </div>
    <div class="d-flex ga-1 mt-1">
        <BlingoTile type="act" text="placeholder text" status="not started" selected="true" />
        <BlingoTile type="understand" text="placeholder text" status="not started" selected="true" />
        <BlingoTile type="act" text="placeholder text" status="not started" selected="true" />
        <BlingoTile type="connect" text="placeholder text" status="not started" selected="true" />
    </div>
</template>

<style scoped></style>
