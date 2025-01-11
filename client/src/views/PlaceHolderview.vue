<script setup lang="ts">
import FriendComponent from '@/components/FriendComponent.vue'
import { ref } from 'vue'

// Define TypeScript interface for friend data
interface FriendEntry {
  avatarIndex: number
  name: string
}

const friendData = ref<FriendEntry[]>([
  { avatarIndex: 1, name: 'Marsha Fisher'},
  { avatarIndex: 2, name: 'Juanita Cormier'},
])
</script>

<template>
  <v-container>
    <h2 class="friend-text text-primaryPink mb-4 mb-sm-3 mb-md-4">Friends</h2>

    <h3 class="section-title2 text-primaryBlue">Friends List</h3>
    <v-row class="friend-scroll">
      <!-- Default Variant -->
      <v-col v-for="(row, index) in friendData" :key="index" cols="12">
        <FriendComponent
          :avatar-index="row.avatarIndex"
          :name="row.name"
        />
      </v-col>
      <!-- Accept/Reject Variant -->
      <v-col v-for="(row, index) in friendData" :key="index" cols="12">
        <FriendComponent
          :avatar-index="row.avatarIndex"
          :name="row.name"
          
        />
      </v-col>
      <!-- Dismiss Variant -->

      <!-- Delete Variant -->
    </v-row>
  </v-container>
</template>

<style scoped>
.friend-text {
  text-align: center;
  font-family: 'Lilita One', cursive;
  font-size: 40px;
  font-weight: 500;
}

.friend-scroll {
  max-height: 400px;
  overflow-y: auto;
}

.section-title {
  margin-top: 16px;
  margin-bottom: 2px;
  font-size: 20px;
  font-family: 'Poppins', cursive;
  text-align: left;
  font-weight: bold;
}

.section-title2 {
  margin-top: 32px;
  margin-bottom: 2px;
  font-size: 20px;
  font-family: 'Poppins', cursive;
  text-align: left;
  font-weight: bold;
}
</style>
