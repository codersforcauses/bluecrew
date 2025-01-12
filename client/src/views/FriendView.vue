<script setup lang="ts">
import FriendComponent from '@/components/FriendComponent.vue'
import { ref } from 'vue'

interface FriendEntry {
  avatarIndex: number
  name: string
}

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

const handleAddFriend = (index: number) => {
  // Handle add friend logic
}
</script>

<template>
  <v-container>
    <h2 class="friend-text text-primaryPink mb-4 mb-sm-3 mb-md-4">Friends</h2>
    
    <h3 class="section-title2 text-primaryBlue">Friend Requests</h3>
    <v-row class="friend-scroll">
      <v-col v-for="(friend, index) in pendingFriends" :key="index" cols="12">
        <FriendComponent
          :avatar-index="friend.avatarIndex"
          :name="friend.name"
          variant="acceptReject"
          @accept="handleAccept(index)"
          @reject="handleReject(index)"
        />
      </v-col>
    </v-row>

    <h3 class="section-title2 text-primaryBlue mt-6">Friends List</h3>
    <v-row class="friend-scroll">
      <v-col v-for="(friend, index) in currentFriends" :key="index" cols="12">
        <FriendComponent
          :avatar-index="friend.avatarIndex"
          :name="friend.name"
          variant="default"
          @dismiss="handleDismiss(index)"
        />
      </v-col>
      <v-col v-for="(friend, index) in currentFriends" :key="index" cols="12">
        <FriendComponent
          :avatar-index="friend.avatarIndex"
          :name="friend.name"
          variant="dismiss"
          @dismiss="handleDismiss(index)"
        />
      </v-col>
      <v-col v-for="(friend, index) in currentFriends" :key="index" cols="12">
        <FriendComponent
          :avatar-index="friend.avatarIndex"
          :name="friend.name"
          variant="delete"
          @delete="handleDelete(index)"
        />
      </v-col>
      <v-col v-for="(friend, index) in currentFriends" :key="index" cols="12">
        <FriendComponent
          :avatar-index="friend.avatarIndex"
          :name="friend.name"
          variant="addFriend"
          @addFriend="handleAddFriend(index)"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
</style>