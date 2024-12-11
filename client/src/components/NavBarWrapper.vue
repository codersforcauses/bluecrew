<script setup lang="ts">
import { useDisplay } from 'vuetify';
import NavBarMobile from '@/components/NavBarMobile.vue';
import NavBarDesktop from '@/components/NavBarDesktop.vue';

const { smAndDown } = useDisplay();
</script>

<template>
  <div>
    <div v-if="smAndDown">
      <NavBarMobile />
    </div>
    <div v-else>
      <NavBarDesktop />
    </div>
  </div>
</template>
