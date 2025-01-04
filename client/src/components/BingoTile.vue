<script setup lang="ts">
defineProps<{
  type: string
  text: string
  status: string
  selected: boolean
}>()
</script>

<template>
    <div class="bg-creamWhite bingo rounded-lg">
        <div>
            <v-img src="man.svg">
            </v-img>
            <p class="text-center">
                {{ text }} 
            </p>
        </div>
    </div>
</template>

<style scoped>
.bingo {
    height: 100px;
    width: 100px;
    border: black 1px solid;
}
</style>

