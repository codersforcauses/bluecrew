# FriendView.vue
<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import FriendComponent from '@/components/FriendComponent.vue'
import WaveBanner from '@/components/WaveBanner.vue'
import { useUserStore } from '@/stores/user'
import server from '@/utils/server'

// Track which subpage is currently active
const currentSubpage = ref<'list' | 'incoming' | 'outgoing'>('list')
const isLoading = ref(true)
const error = ref<string | null>(null)
const searchQuery = ref('')

// What we receive from the API
interface FriendEntry {
  userId: number
  userName: string
  avatar: number
  friendship_id: number
}

interface SearchResult {
  user_data: {
    user_id: number
    username: string
    avatar: number
  }
  status: string
  friendship_id?: number
}

// Current friends list
const currentFriends = ref<FriendEntry[]>([])
const incomingRequests = ref<FriendEntry[]>([])
const outgoingRequests = ref<FriendEntry[]>([])
const searchResults = ref<SearchResult[]>([])

// Computed properties for filtering search results
const existingFriendsResults = computed(() => {
  if (!searchQuery.value) return []
  return currentFriends.value.filter((friend) =>
    friend.userName.toLowerCase().includes(searchQuery.value.toLowerCase()),
  )
})

const filteredSearchResults = computed(() => {
  if (!searchResults.value) return []
  
  // Get list of existing friend IDs
  const existingFriendIds = currentFriends.value.map(friend => friend.userId)
  // Get current user's ID
  const currentUserId = useUserStore().user?.userId 
  
  // Filter out yourself and existing friends
  return searchResults.value.filter(result => 
    result.user_data.user_id !== currentUserId && 
    !existingFriendIds.includes(result.user_data.user_id)
  )
})

// Helper method to determine which variant to show
const getUserVariant = (status: string) => {
  switch (status) {
    case "You have requested friendship.":
      return 'requestSent'
    case "Pending friendship request.":
      return 'accept'
    case "You are friends.":
      return 'details'
    default:
      return 'send'
  }
}

// Fetch functions for each list
const fetchFriends = async () => {
  try {
    const response = await server.get<FriendEntry[]>('/friends/', {
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
    currentFriends.value = response.data
  } catch (err) {
    console.error('Error fetching friends:', err)
    error.value = err instanceof Error ? err.message : 'Failed to fetch friends'
  }
}

const fetchIncomingRequests = async () => {
  try {
    const response = await server.get<FriendEntry[]>('/friends/requests/incoming/', {
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
    incomingRequests.value = response.data
  } catch (err) {
    console.error('Error fetching incoming requests:', err)
  }
}

const fetchOutgoingRequests = async () => {
  try {
    const response = await server.get<FriendEntry[]>('/friends/requests/outgoing/', {
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
    outgoingRequests.value = response.data
  } catch (err) {
    console.error('Error fetching outgoing requests:', err)
  }
}

// Search functionality
const searchUsers = async () => {
  if (!searchQuery.value) {
    searchResults.value = []
    return
  }

  try {
    const response = await server.post<SearchResult[]>('/user-search/', {
      query_string: searchQuery.value
    })
    searchResults.value = response.data
  } catch (err) {
    console.error('Error searching users:', err)
    searchResults.value = []
  }
}

// Watch for search input changes
watch(searchQuery, () => {
  searchUsers()
})

// Initialize data
const fetchAllData = async () => {
  isLoading.value = true
  error.value = null
  try {
    await Promise.all([
      fetchFriends(),
      fetchIncomingRequests(),
      fetchOutgoingRequests()
    ])
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to fetch data'
  } finally {
    isLoading.value = false
  }
}

// Event handlers
const handleAccept = async (userId: number, friendshipId: number) => {
  try {
    await server.post(`/accept-friendship/${friendshipId}/`)
    await fetchAllData()
  } catch (err) {
    console.error('Error accepting friend request:', err)
    error.value = 'Failed to accept friend request'
  }
}

const handleReject = async (userId: number, friendshipId: number) => {
  try {
    await server.delete(`/delete-friendship/${friendshipId}/`)
    await fetchAllData()
  } catch (err) {
    console.error('Error rejecting friend request:', err)
    error.value = 'Failed to reject friend request'
  }
}

const handleDelete = async (userId: number, friendshipId?: number) => {
  console.log('Deleting friendship:', { userId, friendshipId }); // Debug log
  
  if (!friendshipId) {
    console.error('No friendship ID provided for user:', userId);
    error.value = 'Cannot delete friend: Missing friendship ID';
    return;
  }

  try {
    await server.delete(`/delete-friendship/${friendshipId}/`);
    await fetchAllData();
  } catch (err) {
    console.error('Error deleting friend:', err);
    if (err.response) {
      console.error('Error response:', err.response.data); // Log the error response
    }
    error.value = 'Failed to delete friend';
  }
}

const handleDismiss = async (userId: number, friendshipId: number) => {
  try {
    await server.delete(`/delete-friendship/${friendshipId}/`)
    await fetchAllData()
  } catch (err) {
    console.error('Error dismissing request:', err)
    error.value = 'Failed to dismiss request'
  }
}

const handleSend = async (userId: number) => {
  try {
    await server.post(`/request-friendship/${userId}/`)
    await fetchAllData()
    await searchUsers()
  } catch (err) {
    console.error('Error sending friend request:', err)
    error.value = 'Failed to send friend request'
  }
}

const handleDefault = (userId: number) => {
  console.log('View friend details:', userId)
}

onMounted(() => {
  fetchAllData()
})
</script>

<template>
  <v-container class="custom-container">
    <WaveBanner imageSrc="/teambuilding-background.jpg" />
  </v-container>

  <v-container>
    <h2 class="friend-text text-primaryBlue mb-4 mb-sm-3 mb-md-4">Friends</h2>

    <div v-if="isLoading" class="text-center pa-4">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>

    <div v-else-if="error" class="text-center error--text pa-4">
      {{ error }}
    </div>

    <div v-else>
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

      <!-- Regular Content -->
      <div v-if="!searchQuery">
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

        <!-- Friends List -->
        <div v-if="currentSubpage === 'list'">
          <h3 class="section-title2 text-primaryBlue">Friends List</h3>
          <v-row class="friend-scroll">
            <v-col v-for="friend in currentFriends" :key="friend.userId" cols="12">
              <FriendComponent
                :avatar-index="friend.avatar"
                :name="friend.userName"
                variant="delete"
                @delete="handleDelete(friend.userId, friend.friendship_id)"
              />
            </v-col>
          </v-row>
        </div>

        <!-- Incoming Requests -->
        <div v-if="currentSubpage === 'incoming'">
          <h3 class="section-title2 text-primaryBlue">Incoming Requests</h3>
          <v-row class="friend-scroll">
            <v-col v-for="request in incomingRequests" :key="request.userId" cols="12">
              <FriendComponent
                :avatar-index="request.avatar"
                :name="request.userName"
                variant="acceptReject"
                @accept="handleAccept(request.userId, request.friendship_id)"
                @reject="handleReject(request.userId, request.friendship_id)"
              />
            </v-col>
          </v-row>
        </div>

        <!-- Outgoing Requests -->
        <div v-if="currentSubpage === 'outgoing'">
          <h3 class="section-title2 text-primaryBlue">Outgoing Requests</h3>
          <v-row class="friend-scroll">
            <v-col v-for="request in outgoingRequests" :key="request.userId" cols="12">
              <FriendComponent
                :avatar-index="request.avatar"
                :name="request.userName"
                variant="dismiss"
                @dismiss="handleDismiss(request.userId, request.friendship_id)"
              />
            </v-col>
          </v-row>
        </div>
      </div>

      <!-- Search Results -->
      <div v-else>
        <!-- Existing Friends Section -->
        <div v-if="existingFriendsResults.length > 0">
          <h3 class="section-title2 text-primaryBlue">
            Existing Friends - {{ existingFriendsResults.length }}
          </h3>
          <v-row class="friend-scroll">
            <v-col v-for="friend in existingFriendsResults" :key="friend.userId" cols="12">
              <FriendComponent
                :avatar-index="friend.avatar"
                :name="friend.userName"
                variant="details"
                @default="handleDefault(friend.userId)"
              />
            </v-col>
          </v-row>
        </div>

        <!-- Other Users Section -->
        <div v-if="filteredSearchResults.length > 0">
          <h3 class="section-title2 text-primaryBlue">
            Other Users - {{ filteredSearchResults.length }}
          </h3>
          <v-row class="friend-scroll">
            <v-col v-for="result in filteredSearchResults" :key="result.user_data.user_id" cols="12">
              <FriendComponent
                :avatar-index="result.user_data.avatar"
                :name="result.user_data.username"
                :variant="getUserVariant(result.status)"
                @send="handleSend(result.user_data.user_id)"
                @accept="handleAccept(result.user_data.user_id, result.friendship_id)"
                @reject="result.friendship_id && handleReject(result.user_data.user_id, result.friendship_id)"
                @dismiss="result.friendship_id && handleDismiss(result.user_data.user_id, result.friendship_id)"
                @default="handleDefault(result.user_data.user_id)"
              />
            </v-col>
          </v-row>
        </div>
      </div>
    </div>
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

.font-poppins {
  font-family: 'Poppins', cursive !important;
  font-weight: bold !important;
}
</style>