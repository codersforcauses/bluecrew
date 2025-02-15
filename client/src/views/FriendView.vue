<script setup lang="ts">
import { ref, computed } from 'vue'
import FriendComponent from '@/components/FriendComponent.vue'
import WaveBanner from '@/components/WaveBanner.vue'
import { useMessageStore } from '@/stores/message'

// Track which subpage is currently active
const currentSubpage = ref<'list' | 'incoming' | 'outgoing'>('list')
const messageStore = useMessageStore()

interface FriendEntry {
  id: number
  avatarIndex: number
  name: string
}
const handleDismiss = (id: number) => {
  messageStore.showMessage('Success', `Dismissed friend request from "${id}"`, 'success')
}

// Current friends list
const currentFriends = ref<FriendEntry[]>([
  { id: 1, avatarIndex: 3, name: 'John Smith' },
  { id: 2, avatarIndex: 4, name: 'Sarah Johnson' },
])

// Incoming friend requests
const incomingRequests = ref<FriendEntry[]>([
  { id: 3, avatarIndex: 1, name: 'Marsha Fisher' },
  { id: 4, avatarIndex: 2, name: 'Juanita Cormier' },
])

// Outgoing friend requests
const outgoingRequests = ref<FriendEntry[]>([
  { id: 5, avatarIndex: 5, name: 'Michael Brown' },
  { id: 6, avatarIndex: 0, name: 'Emma Davis' },
])

// Search functionality
const searchQuery = ref('')

// Computed properties for filtering search results
const existingFriendsResults = computed(() => {
  if (!searchQuery.value) return []
  return currentFriends.value.filter((friend) =>
    friend.name.toLowerCase().includes(searchQuery.value.toLowerCase()),
  )
})

const otherUsersResults = computed(() => {
  if (!searchQuery.value) return []
  // Mock search results - replace with actual search logic
  const mockResults = [
    { id: 7, avatarIndex: 0, name: 'Alex Thompson', status: 'none' },
    { id: 8, avatarIndex: 1, name: 'Jessica Wilson', status: 'outgoing' },
    { id: 9, avatarIndex: 2, name: 'Mike Johnson', status: 'incoming' },
  ]
  return mockResults.filter((user) =>
    user.name.toLowerCase().includes(searchQuery.value.toLowerCase()),
  )
})

// Helper method to determine which variant to show
const getUserVariant = (user: { status: string }) => {
  switch (user.status) {
    case 'outgoing':
      return 'requestSent'
    case 'incoming':
      return 'accept'
    default:
      return 'send'
  }
}

// Event handlers
const handleAccept = (id: number) => {
  messageStore.showMessage('Success', `Accepted friend request from "${id}"`, 'success')
}

const handleReject = (id: number) => {
  messageStore.showMessage('Success', `Rejected friend request from "${id}"`, 'success')
}

const handleDelete = (id: number) => {
  messageStore.showMessage('Success', `Deleted friend: "${id}"`, 'success')
}

const handledefault = (id: number) => {
  messageStore.showMessage('Success', `View default: "${id}"`, 'success')
}

const handleSend = (id: number) => {
  messageStore.showMessage('Success', `Sent friend request to "${id}"`, 'success')
}
</script>

<template>
  <v-container class="custom-container">
    <WaveBanner imageSrc="/teambuilding-background.jpg" />
  </v-container>

  <v-container>
    <h2 class="friend-text text-primaryBlue mb-4 mb-sm-3 mb-md-4">Friends</h2>

    <!-- Search Bar -->
    <v-text-field
      v-model="searchQuery"
      prepend-inner-icon="mdi-magnify"
      label="Search users"
      class="mb-6 search-field text-center"
      hide-default
      single-line
      variant="outlined"
      color="primaryBlue"
      bg-color="creamWhite"
      clearable
    />

    <!-- Only show navigation and regular content if not searching -->
    <template v-if="!searchQuery">
      <!-- Navigation Buttons -->
      <v-btn-group class="w-100 mb-6">
        <v-btn
          :color="currentSubpage === 'list' ? 'primaryGreen' : 'primaryBlue'"
          @click="currentSubpage = 'list'"
          class="flex-grow-1 text-caption text-sm-subtitle-2 font-poppins"
        >
          Friends List
        </v-btn>
        <v-btn
          :color="currentSubpage === 'incoming' ? 'primaryGreen' : 'primaryBlue'"
          @click="currentSubpage = 'incoming'"
          class="flex-grow-1 text-caption text-sm-subtitle-2 font-poppins"
        >
          Incoming
        </v-btn>
        <v-btn
          :color="currentSubpage === 'outgoing' ? 'primaryGreen' : 'primaryBlue'"
          @click="currentSubpage = 'outgoing'"
          class="flex-grow-1 text-caption text-sm-subtitle-2 font-poppins"
        >
          Outgoing
        </v-btn>
      </v-btn-group>

      <!-- Regular Content -->
      <div v-if="currentSubpage === 'list'">
        <h3 class="section-title2 text-primaryBlue">Friends List</h3>
        <v-row class="friend-scroll">
          <v-col v-for="friend in currentFriends" :key="friend.id" cols="12">
            <FriendComponent
              :avatar-index="friend.avatarIndex"
              :name="friend.name"
              variant="delete"
              @delete="handleDelete(friend.id)"
            />
          </v-col>
        </v-row>
      </div>

      <div v-if="currentSubpage === 'incoming'">
        <h3 class="section-title2 text-primaryBlue">Incoming Requests</h3>
        <v-row class="friend-scroll">
          <v-col v-for="request in incomingRequests" :key="request.id" cols="12">
            <FriendComponent
              :avatar-index="request.avatarIndex"
              :name="request.name"
              variant="acceptReject"
              @accept="handleAccept(request.id)"
              @reject="handleReject(request.id)"
            />
          </v-col>
        </v-row>
      </div>

      <div v-if="currentSubpage === 'outgoing'">
        <h3 class="section-title2 text-primaryBlue">Outgoing Requests</h3>
        <v-row class="friend-scroll">
          <v-col v-for="request in outgoingRequests" :key="request.id" cols="12">
            <FriendComponent
              :avatar-index="request.avatarIndex"
              :name="request.name"
              variant="dismiss"
              @dismiss="handleDismiss(request.id)"
            />
          </v-col>
        </v-row>
      </div>
    </template>

    <!-- Search Results -->
    <template v-if="searchQuery">
      <!-- Existing Friends Section -->
      <div v-if="existingFriendsResults.length > 0">
        <h3 class="section-title2 text-primaryBlue">
          Existing Friends - {{ existingFriendsResults.length }}
        </h3>
        <v-row class="friend-scroll">
          <v-col v-for="result in existingFriendsResults" :key="result.id" cols="12">
            <FriendComponent
              :avatar-index="result.avatarIndex"
              :name="result.name"
              variant="default"
              @default="handledefault(result.id)"
            />
          </v-col>
        </v-row>
      </div>

      <!-- Other Users Section -->
      <div v-if="otherUsersResults.length > 0">
        <h3 class="section-title2 text-primaryBlue">
          Other Users - {{ otherUsersResults.length }}
        </h3>
        <v-row class="friend-scroll">
          <v-col v-for="result in otherUsersResults" :key="result.id" cols="12">
            <FriendComponent
              :avatar-index="result.avatarIndex"
              :name="result.name"
              :variant="getUserVariant(result)"
              @send="handleSend(result.id)"
              @accept="handleAccept(result.id)"
            />
          </v-col>
        </v-row>
      </div>
    </template>
  </v-container>
</template>

<style scoped>
.custom-container {
  max-width: 100%;
  padding: 0;
}

.friend-text {
  text-align: center;
  font-family: 'Lilita One', cursive;
  font-size: 40px;
  font-weight: 500;
}

.section-title2 {
  margin-top: 32px;
  margin-bottom: 2px;
  font-size: 20px;
  font-family: 'Poppins', cursive;
  text-align: left;
  font-weight: bold;
}

.friend-scroll {
  max-height: 400px;
  overflow-y: auto;
}

.search-field {
  max-width: 100%;
}

/* Custom scrollbar styling */
.friend-scroll::-webkit-scrollbar {
  width: 8px;
}

.friend-scroll::-webkit-scrollbar-track {
  background: rgb(var(--v-theme-creamWhite));
}

.friend-scroll::-webkit-scrollbar-thumb {
  background: rgb(var(--v-theme-primaryBlue));
  border-radius: 4px;
}

.friend-scroll::-webkit-scrollbar-thumb:hover {
  background: rgb(var(--v-theme-primaryGreen));
}

.font-poppins {
  font-family: 'Poppins', cursive !important;
  font-weight: bold !important;
}
</style>
