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
    <v-col :class="[isHighlighted ? 'bg-primaryPink' : 'bg-creamWhite text-primaryGrey']" class="rounded-lg d-flex ga-3 px-5 align-center">
        <v-text class="font-weight-bold">{{ rank }}</v-text>
        <v-img
            class="rounded-circle "
            max-height="32"
            max-width="32"
            min-width="32"
            cover
            src="https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg"
        ></v-img>
        <v-text class="me-auto font-weight-bold truncate-single-line">{{ name }}</v-text>
        <v-text :class="[isHighlighted ? 'font-weight-bold' : '' ]" class="text-right points">{{ points }} pts</v-text>
    </v-col>
</template>

<style scoped>
.truncate-single-line {
    white-space: nowrap;        
    overflow: hidden;          
    text-overflow: ellipsis;     
}

.points {
    white-space: nowrap;
}
</style>
