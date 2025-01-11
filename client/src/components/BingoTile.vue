<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
    type: "connect" | "understand" | "act"
    text: string
    status: "not started" | "started" | "completed"
    selected: boolean
}>()


const icon = computed(() => {
    switch (props.type) {
        case "act":
            return "walking.svg"
        case "understand":
            return "brain.svg"
        default:
            return "link.svg"
    }
})


const backgroundColour = computed(() => {
    switch (props.status) {
        case "started":
            return "bg-primaryPink"
        case "completed":
            return "bg-lightBlue"
        default:
            return "bg-creamWhite"
    }
})

const textColour = computed(() => {
    switch (props.status) {
        case "started":
        case "completed":
            return "text-primaryWhite"
        default:
            return "text-primaryBlack"
    }
})

const iconBackground = computed(() => {
    switch (backgroundColour.value) {
        case "bg-creamWhite":
            return "dark"
        default:
            return "light"
    }
})

</script>

<template>
    <div :class="[backgroundColour, textColour]" class="outer-tile rounded-lg d-flex flex-column align-center ">
        <v-img class="icon" :class="iconBackground" :src="icon" />
        <p class="tile-text text-center font-weight-bold">
            {{ text }}
        </p>

    </div>
</template>

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
