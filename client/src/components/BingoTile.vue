<script setup lang="ts">

defineProps<{
    type: string
    text: string
    status: string
    selected: boolean
}>()

// need to download svgs and change out srcs and names
function getIconSrc(type: string): string {
    switch (type) {
        case "thing1":
            return "man.svg"
        case "thing2":
            return "thing2.svg"
        default:
            return "man.svg"
    }
}


</script>

<!-- Added flex and text styling, call function for name of icon src, add image width -->
<template>
    <div class="bg-creamWhite outer-tile rounded-lg d-flex flex-column align-center ">

        <v-img :src="getIconSrc(type)" :style="{ width: '30%' }" />
    <p class=" tile-text text-center font-weight-bold text-primaryGrey">
            {{ text }}
        </p>

    </div>
</template>

<!-- changed sizes to rem to be proportional and added padding, improved naming??, random finicky fixes -->
<style scoped>
.outer-tile {
    height: 5rem;
    width: 5rem;
    border: #4F4F4F 0.1rem solid;
    padding: 0.5rem;
}

.tile-text {
    font-size: 0.6rem;
    line-height: 1.2
}
</style>
