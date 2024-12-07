<script setup lang="ts">
import { RouterView } from 'vue-router'
import RegisterModal from './components/RegisterModal.vue'
import { ref } from 'vue'
const dialog = ref(false)
</script>

<template>
  <div class="pa-4 text-center">
    <v-dialog max-width="30%" v-model="dialog" scrollable persistent>
      <template v-slot:activator="{ props: activatorProps }">
        <v-btn class="bg-primaryBlue" v-bind="activatorProps" text="Registration"></v-btn>
      </template>

      <v-card>
        <v-card-text style="height: auto; overflow-y: auto">
          <RegisterModal @close="dialog = false" />
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
  <RouterView />
</template>

<style scoped></style>
