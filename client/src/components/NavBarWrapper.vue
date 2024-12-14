<script setup lang="ts">
import { useDisplay } from 'vuetify';
import NavBarMobile from '@/components/NavBarMobile.vue';
import NavBarDesktop from '@/components/NavBarDesktop.vue';

const { smAndUp } = useDisplay();
</script>

<template>
  <div>
    <div v-if="smAndUp">
      <NavBarDesktop />
    </div>
    <div v-else>
      <NavBarMobile />
    </div>
  </div>
</template>
