<script setup lang="ts">
import { ref, onMounted } from 'vue'
import BluecrewFooter from '@/components/BluecrewFooter.vue'
import NavBarWrapper from '@/components/NavBarWrapper.vue'
import type { NavBarWrapperExpose } from '@/components/NavBarWrapper.vue'

const navBarHeight = ref(0)
// Introduce instance from NavBarWrapper
const navBarWrapperInstance = ref<NavBarWrapperExpose | null>(null)

onMounted(() => {
  if (navBarWrapperInstance.value) {
    navBarHeight.value = navBarWrapperInstance.value.navBarHeight
  }
})
</script>

<template>
  <v-app>
    <!-- Navigation Bar -->
    <NavBarWrapper ref="navBarWrapperInstance" />

    <v-main :style="{ paddingTop: navBarHeight + 'px' }">
      <RouterView />
    </v-main>

    <!-- Footer -->
    <BluecrewFooter />
  </v-app>
</template>

<style scoped></style>
