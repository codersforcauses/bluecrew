<script setup lang="ts">
import FriendComponent from '@/components/FriendComponent.vue'
import { ref } from 'vue'

// Define TypeScript interface for friend data
interface FriendEntry {
  avatarIndex: number
  name: string
}

// Separate arrays for different friend categories
const pendingFriends = ref<FriendEntry[]>([
  { avatarIndex: 1, name: 'Marsha Fisher'},
  { avatarIndex: 2, name: 'Juanita Cormier'},
])

const currentFriends = ref<FriendEntry[]>([
  { avatarIndex: 3, name: 'John Smith'},
  { avatarIndex: 4, name: 'Sarah Johnson'},
])


const handleAccept = (index: number) => {
  // Handle accept logic
}

const handleReject = (index: number) => {
  // Handle reject logic
}

const handleDismiss = (index: number) => {
  // Handle dismiss logic
}

const handleDelete = (index: number) => {
  // Handle delete logic
}
</script>

<template>
  <v-container>
    <h2 class="friend-text text-primaryPink mb-4 mb-sm-3 mb-md-4">Friends</h2>
    
    <!-- Pending Friend Requests Section -->
    <h3 class="section-title2 text-primaryBlue">Friend Requests</h3>
    <v-row class="friend-scroll">
      <v-col v-for="(friend, index) in pendingFriends" :key="index" cols="12">
        <FriendComponent
          :avatar-index="friend.avatarIndex"
          :name="friend.name"
        >
          <template #acceptreject>
            <v-icon 
              icon="mdi-check" 
              color="success" 
              @click="handleAccept(index)"
              class="cursor-pointer"
            />
            <v-icon 
              icon="mdi-close" 
              color="error" 
              @click="handleReject(index)"
              class="cursor-pointer"
            />
          </template>
        </FriendComponent>
      </v-col>
    </v-row>

    <!-- Current Friends Section -->
    <h3 class="section-title2 text-primaryBlue mt-6">Friends List</h3>
    <v-row class="friend-scroll">
      <!-- Dismiss Variant -->
      <v-col v-for="(friend, index) in currentFriends" :key="index" cols="12">
        <FriendComponent
          :avatar-index="friend.avatarIndex"
          :name="friend.name"
        >
          <template #dismiss>
            <v-btn
              color="primaryBlue"
              variant="flat"
              density="comfortable"
              @click="handleDismiss(index)"
            >
              Dismiss
            </v-btn>
          </template>
        </FriendComponent>
      </v-col>

      <!-- Delete Variant -->
      <v-col v-for="(friend, index) in currentFriends" :key="index" cols="12">
        <FriendComponent
          :avatar-index="friend.avatarIndex"
          :name="friend.name"
          @confirm-delete="handleDelete(index)"
        >
          <template #delete>
            <v-btn
              color="primaryPink"
              variant="flat"
              density="comfortable"
            >
              Delete
            </v-btn>
          </template>
        </FriendComponent>
      </v-col>

      <!-- Delete Variant -->
      <v-col v-for="(friend, index) in currentFriends" :key="index" cols="12">
        <FriendComponent
          :avatar-index="friend.avatarIndex"
          :name="friend.name"
          @confirm-delete="handleDelete(index)"
        >
          <template #delete>
            <v-btn
              color="primaryPink"
              variant="flat"
              density="comfortable"
            >
              Delete
            </v-btn>
          </template>
        </FriendComponent>
      </v-col>

      <!-- Add Variant -->
      <v-col v-for="(friend, index) in currentFriends" :key="index" cols="12">
        <FriendComponent
          :avatar-index="friend.avatarIndex"
          :name="friend.name"
          @confirm-delete="handleDelete(index)"
        >
          <template #addfriend>
            <v-btn
              color="primaryPink"
              variant="flat"
              density="comfortable"
            >
              Add Friend
            </v-btn>
          </template>
        </FriendComponent>
      </v-col>

      <!-- Accept Variant -->
      <v-col v-for="(friend, index) in currentFriends" :key="index" cols="12">
        <FriendComponent
          :avatar-index="friend.avatarIndex"
          :name="friend.name"
          @confirm-delete="handleDelete(index)"
        >
          <template #accept>
            <v-btn
              color="primaryPink"
              variant="flat"
            >
              Accept
            </v-btn>
          </template>
        </FriendComponent>
      </v-col>

      <!-- Delete Variant -->
      <v-col v-for="(friend, index) in currentFriends" :key="index" cols="12">
        <FriendComponent
          :avatar-index="friend.avatarIndex"
          :name="friend.name"
          @confirm-delete="handleDelete(index)"
        >
          <template #default>
          </template>
        </FriendComponent>
      </v-col>
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

.cursor-pointer {
  cursor: pointer;
}
</style>