<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import FriendComponent from '@/components/FriendComponent.vue'
import WaveBanner from '@/components/WaveBanner.vue'
import server from '@/utils/server'

// Types
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

type FriendAction = 'accept' | 'delete' | 'dismiss' | 'reject' | 'send'
type SubPage = 'list' | 'incoming' | 'outgoing'

// State
const currentSubpage = ref<SubPage>('list')
const isLoading = ref(true)
const error = ref<string | null>(null)
const searchQuery = ref('')
const currentFriends = ref<FriendEntry[]>([])
const incomingRequests = ref<FriendEntry[]>([])
const outgoingRequests = ref<FriendEntry[]>([])
const searchResults = ref<SearchResult[]>([])

// Computed
const existingFriendsResults = computed(() =>
  searchQuery.value
    ? currentFriends.value.filter((friend) =>
        friend.userName.toLowerCase().includes(searchQuery.value.toLowerCase()),
      )
    : [],
)

const filteredSearchResults = computed(
  () =>
    searchResults.value?.filter(
      (result) =>
        !currentFriends.value.some((friend) => friend.userId === result.user_data.user_id),
    ) ?? [],
)

// Helpers
const getUserVariant = (status: string) => {
  switch (status) {
    case 'You have requested friendship.':
      return 'requestSent'
    case 'Pending friendship request.':
      return 'accept'
    case 'You are friends.':
      return 'details'
    default:
      return 'send'
  }
}

// Data fetching
const fetchFriendsData = async () => {
  isLoading.value = true
  error.value = null

  try {
    const [friendsResponse, incomingResponse, outgoingResponse] = await Promise.all([
      server.get<FriendEntry[]>('/friends/'),
      server.get<FriendEntry[]>('/friends/requests/incoming/'),
      server.get<FriendEntry[]>('/friends/requests/outgoing/'),
    ])

    currentFriends.value = friendsResponse.data
    incomingRequests.value = incomingResponse.data
    outgoingRequests.value = outgoingResponse.data
  } catch (err) {
    error.value = 'Failed to fetch friends data'
  } finally {
    isLoading.value = false
  }
}

const searchUsers = async () => {
  if (!searchQuery.value) {
    searchResults.value = []
    return
  }

  try {
    const response = await server.post<SearchResult[]>('/user-search/', {
      query_string: searchQuery.value,
    })
    searchResults.value = response.data
  } catch (err) {
    searchResults.value = []
    error.value = 'Failed to search users'
  }
}

// Event handlers
const handleFriendAction = async (action: FriendAction, userId: number, friendshipId?: number) => {
  try {
    switch (action) {
      case 'accept':
        await server.post(`/accept-friendship/${friendshipId}/`)
        break
      case 'send':
        await server.post(`/request-friendship/${userId}/`)
        break
      case 'delete':
      case 'dismiss':
      case 'reject':
        await server.delete(`/delete-friendship/${friendshipId}/`)
        break
    }
    await fetchFriendsData()
    if (action === 'send') await searchUsers()
  } catch (err) {
    error.value = `Failed to ${action} friend${action === 'send' ? ' request' : ''}`
  }
}

// Lifecycle
watch(searchQuery, searchUsers)
onMounted(fetchFriendsData)
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
        <v-btn-group class="w-100 mb-6">
          <v-btn
            v-for="page in ['list', 'incoming', 'outgoing']"
            :key="page"
            :color="currentSubpage === page ? 'primaryGreen' : 'primaryBlue'"
            @click="currentSubpage = page"
            class="flex-grow-1 text-caption text-sm-subtitle-2 font-poppins"
          >
            {{ page.charAt(0).toUpperCase() + page.slice(1) }}
          </v-btn>
        </v-btn-group>

        <!-- Friends List -->
        <div v-if="currentSubpage === 'list'">
          <h3 class="section-title2 text-primaryBlue">Friends List</h3>
          <v-row v-if="currentFriends.length === 0" class="text-center my-6">
            <v-col>
              <p class="text-primaryBlue font-italic">
                Looks like you haven't added any friends yet!
                <br />Start by searching for users to connect with.
              </p>
            </v-col>
          </v-row>
          <v-row v-else class="friend-scroll">
            <v-col v-for="friend in currentFriends" :key="friend.userId" cols="12">
              <FriendComponent
                :avatar-index="friend.avatar"
                :name="friend.userName"
                variant="delete"
                @delete="handleFriendAction('delete', friend.userId, friend.friendship_id)"
              />
            </v-col>
          </v-row>
        </div>

        <!-- Incoming Requests -->
        <div v-if="currentSubpage === 'incoming'">
          <h3 class="section-title2 text-primaryBlue">Incoming Requests</h3>
          <v-row v-if="incomingRequests.length === 0" class="text-center my-6">
            <v-col>
              <p class="text-primaryBlue font-italic">
                Oh no! No friend requests yet.
                <br />Keep exploring and connecting with others!
              </p>
            </v-col>
          </v-row>
          <v-row v-else class="friend-scroll">
            <v-col v-for="request in incomingRequests" :key="request.userId" cols="12">
              <FriendComponent
                :avatar-index="request.avatar"
                :name="request.userName"
                variant="acceptReject"
                @accept="handleFriendAction('accept', request.userId, request.friendship_id)"
                @reject="handleFriendAction('reject', request.userId, request.friendship_id)"
              />
            </v-col>
          </v-row>
        </div>

        <!-- Outgoing Requests -->
        <div v-if="currentSubpage === 'outgoing'">
          <h3 class="section-title2 text-primaryBlue">Outgoing Requests</h3>
          <v-row v-if="outgoingRequests.length === 0" class="text-center my-6">
            <v-col>
              <p class="text-primaryBlue font-italic">
                No pending friend requests at the moment.
                <br />Keep exploring and sending connection requests!
              </p>
            </v-col>
          </v-row>
          <v-row v-else class="friend-scroll">
            <v-col v-for="request in outgoingRequests" :key="request.userId" cols="12">
              <FriendComponent
                :avatar-index="request.avatar"
                :name="request.userName"
                variant="dismiss"
                @dismiss="handleFriendAction('dismiss', request.userId, request.friendship_id)"
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
            <v-col
              v-for="result in filteredSearchResults"
              :key="result.user_data.user_id"
              cols="12"
            >
              <FriendComponent
                :avatar-index="result.user_data.avatar"
                :name="result.user_data.username"
                :variant="getUserVariant(result.status)"
                @send="handleFriendAction('send', result.user_data.user_id)"
                @accept="
                  handleFriendAction('accept', result.user_data.user_id, result.friendship_id)
                "
                @reject="
                  result.friendship_id &&
                    handleFriendAction('reject', result.user_data.user_id, result.friendship_id)
                "
                @dismiss="
                  result.friendship_id &&
                    handleFriendAction('dismiss', result.user_data.user_id, result.friendship_id)
                "
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
