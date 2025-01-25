# FriendView.vue
<script setup lang="ts">
import { ref, computed } from 'vue'
import { useDisplay } from 'vuetify'
import FriendComponent from '@/components/FriendComponent.vue'

// Track which subpage is currently active for mobile view
const currentSubpage = ref<'list' | 'incoming' | 'outgoing'>('list')

// Get viewport info from Vuetify for responsive design
const { mobile } = useDisplay()

interface FriendEntry {
  id: number
  avatarIndex: number
  name: string
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
  { id: 6, avatarIndex: 6, name: 'Emma Davis' },
])

// Search functionality
const searchQuery = ref('')
const searchResults = computed(() => {
  if (!searchQuery.value) return []
  // Mock search results - replace with actual search logic
  return [
    { id: 7, avatarIndex: 0, name: 'Alex Thompson' },
    { id: 8, avatarIndex: 1, name: 'Jessica Wilson' },
  ]
})

// Event handlers
const handleAccept = (id: number) => {
  console.log('Accept friend request:', id)
}

const handleReject = (id: number) => {
  console.log('Reject friend request:', id)
}

const handleDelete = (id: number) => {
  console.log('Delete friend:', id)
}

const handleAddFriend = (id: number) => {
  console.log('Add friend:', id)
}

const handleDismiss = (id: number) => {
  console.log('Dismiss request:', id)
}
</script>

<template>
  <v-container>
    <h2 class="friend-text text-primaryPink mb-4 mb-sm-3 mb-md-4">Friends</h2>

    <!-- Search Bar -->
    <v-text-field
      v-model="searchQuery"
      prepend-inner-icon="mdi-magnify"
      label="Search users"
      single-line
      hide-details
      class="mb-6 search-field"
      variant="outlined"
    ></v-text-field>

    <!-- Mobile View -->
    <template v-if="mobile">
      <!-- Navigation Buttons -->
      <v-btn-group class="w-100 mb-6">
        <v-btn
          :color="currentSubpage === 'list' ? 'primaryPink' : 'primaryBlue'"
          @click="currentSubpage = 'list'"
          class="flex-grow-1"
        >
          Friends List
        </v-btn>
        <v-btn
          :color="currentSubpage === 'incoming' ? 'primaryPink' : 'primaryBlue'"
          @click="currentSubpage = 'incoming'"
          class="flex-grow-1"
        >
          Incoming
        </v-btn>
        <v-btn
          :color="currentSubpage === 'outgoing' ? 'primaryPink' : 'primaryBlue'"
          @click="currentSubpage = 'outgoing'"
          class="flex-grow-1"
        >
          Outgoing
        </v-btn>
      </v-btn-group>

      <!-- Mobile Content -->
      <div v-if="currentSubpage === 'list'">
        <h3 class="section-title2 text-primaryBlue mb-4">Friends List</h3>
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
        <h3 class="section-title2 text-primaryBlue mb-4">Incoming Requests</h3>
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
        <h3 class="section-title2 text-primaryBlue mb-4">Outgoing Requests</h3>
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

    <!-- Desktop View -->
    <template v-else>
      <div class="d-flex gap-6">
        <!-- Left Column -->
        <div class="flex-grow-1">
          <!-- Friend Requests Section -->
          <h3 class="section-title2 text-primaryBlue mb-4">Friend Requests</h3>
          <v-row class="friend-scroll mb-6">
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

          <!-- Friends List Section -->
          <h3 class="section-title2 text-primaryBlue mb-4">Friends List</h3>
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

        <!-- Right Column (Search Results) -->
        <div v-if="searchQuery" class="search-results">
          <h3 class="section-title2 text-primaryBlue mb-4">Search Results</h3>
          <v-row class="friend-scroll">
            <v-col v-for="result in searchResults" :key="result.id" cols="12">
              <FriendComponent
                :avatar-index="result.avatarIndex"
                :name="result.name"
                variant="addFriend"
                @add-friend="handleAddFriend(result.id)"
              />
            </v-col>
          </v-row>
        </div>
      </div>
    </template>
  </v-container>
</template>

<style scoped>
.friend-text {
  font-family: 'Poppins', sans-serif;
  font-weight: bold;
  font-size: 2rem;
}

.section-title2 {
  font-family: 'Poppins', sans-serif;
  font-weight: bold;
  font-size: 1.5rem;
}

.search-field {
  max-width: 600px;
}

.search-results {
  width: 300px;
  min-width: 300px;
}

.friend-scroll {
  max-height: calc(100vh - 400px);
  overflow-y: auto;
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
  background: rgb(var(--v-theme-primaryPink));
}
</style>