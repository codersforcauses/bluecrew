<script setup lang="ts">
import { RouterView } from 'vue-router'
import RegisterModal from './components/RegisterModal.vue'
import { ref } from 'vue'
const dialog = ref(false)
</script>

<template>
  <div class="pa-4 text-center">
    <v-dialog max-width="30%" v-model="dialog" scrollable>
      <template v-slot:activator="{ props: activatorProps }">
        <v-btn id="button" v-bind="activatorProps" text="Registration"></v-btn>
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

<style scoped>
#button {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.16);
}
</style>
