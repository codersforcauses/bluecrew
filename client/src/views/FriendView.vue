<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import FriendComponent from '@/components/FriendComponent.vue'
import WaveBanner from '@/components/WaveBanner.vue'
import server from '@/utils/server'
import { useMessageStore } from '@/stores/message'

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
const searchQuery = ref('')
const currentFriends = ref<FriendEntry[]>([])
const incomingRequests = ref<FriendEntry[]>([])
const outgoingRequests = ref<FriendEntry[]>([])
const searchResults = ref<SearchResult[]>([])
const searchResultsLoading = ref(false)
const messageStore = useMessageStore()

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

const fetchFriendsData = async () => {
  isLoading.value = true

  try {
    const response = await server.get<{
      current_friends: FriendEntry[]
      incoming_requests: FriendEntry[]
      outgoing_requests: FriendEntry[]
    }>('/friends/all/')

    // Update all three ref values from the single response
    currentFriends.value = response.data.current_friends
    incomingRequests.value = response.data.incoming_requests
    outgoingRequests.value = response.data.outgoing_requests
  } catch {
    messageStore.showMessage('Error', 'Failed to fetch friends data', 'error')
  } finally {
    isLoading.value = false
  }
}

const searchUsers = async () => {
  if (!searchQuery.value) {
    searchResults.value = []
    return
  }
  searchResultsLoading.value = true

  try {
    const response = await server.post<SearchResult[]>('/user-search/', {
      query_string: searchQuery.value,
    })
    searchResults.value = response.data
  } catch {
    searchResults.value = []
    messageStore.showMessage('Error', 'Failed to search users', 'error')
  } finally {
    searchResultsLoading.value = false
  }
}

// Event handlers
const handleFriendAction = async (
  action: FriendAction,
  userId: number,
  updateSearchResults: boolean,
  arrayIndex: number,
  friendshipId?: number,
) => {
  try {
    let successMessage = ''

    switch (action) {
      case 'accept':
        await server.post(`/accept-friendship/${friendshipId}/`)
        if (updateSearchResults) {
          searchResults.value[arrayIndex].status = 'You are friends.'
          await fetchFriendsData()
        } else {
          // Move friend from incomingRequests to currentFriends
          const acceptedFriend = incomingRequests.value[arrayIndex]
          incomingRequests.value.splice(arrayIndex, 1)
          currentFriends.value.push(acceptedFriend)
        }
        successMessage = 'Friend request accepted!'
        break

      case 'delete':
        await server.delete(`/delete-friendship/${friendshipId}/`)
        if (updateSearchResults) {
          searchResults.value[arrayIndex].status = 'You are not friends.'
          await fetchFriendsData()
        } else {
          currentFriends.value.splice(arrayIndex, 1)
        }
        successMessage = 'Friend removed'
        break

      case 'dismiss':
      case 'reject':
        await server.delete(`/delete-friendship/${friendshipId}/`)
        if (updateSearchResults) {
          searchResults.value[arrayIndex].status = 'You are not friends.'
          await fetchFriendsData()
        } else {
          const array = action === 'dismiss' ? outgoingRequests : incomingRequests
          array.value.splice(arrayIndex, 1)
        }
        successMessage = action === 'dismiss' ? 'Request cancelled' : 'Request rejected'
        break

      case 'send':
        await server.post(`/request-friendship/${userId}/`)
        if (updateSearchResults) {
          searchResults.value[arrayIndex].status = 'You have requested friendship.'
          await fetchFriendsData()
        }
        successMessage = 'Friend request sent!'
        break
    }

    messageStore.showMessage('Success', successMessage, 'success')
  } catch {
    messageStore.showMessage(
      'Error',
      `Failed to ${action} friend${action === 'send' ? ' request' : ''}`,
      'error',
    )
  }
}

// Lifecycle
watch(searchQuery, searchUsers)
onMounted(fetchFriendsData)
</script>

<template>
  <WaveBanner
    imageSrc="/teambuilding-background.jpg"
    altText="Volunteers making sandcastles together"
  />
  <v-container>
    <h2 class="friend-text text-primaryBlue mb-4 mb-sm-3 mb-md-4">Friends</h2>

    <div v-if="isLoading" class="text-center pa-4">
      <v-progress-circular indeterminate color="primary" />
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
            v-for="page in ['list', 'incoming', 'outgoing'] as const"
            :key="page"
            :color="currentSubpage === page ? 'primaryGreen' : 'primaryBlue'"
            @click="currentSubpage = page"
            class="flex-grow-1 text-caption text-sm-subtitle-2 font-poppins"
          >
            {{ page === 'list' ? 'Friend List' : page.charAt(0).toUpperCase() + page.slice(1) }}
          </v-btn>
        </v-btn-group>

        <!-- Friends List -->
        <v-sheet v-if="currentSubpage === 'list'">
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
            <v-col v-for="(friend, index) in currentFriends" :key="friend.userId" cols="12">
              <FriendComponent
                :avatar-index="friend.avatar"
                :name="friend.userName"
                variant="delete"
                @delete="
                  handleFriendAction('delete', friend.userId, false, index, friend.friendship_id)
                "
              />
            </v-col>
          </v-row>
        </v-sheet>

        <!-- Incoming Requests -->
        <v-sheet v-if="currentSubpage === 'incoming'">
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
            <v-col v-for="(request, index) in incomingRequests" :key="request.userId" cols="12">
              <FriendComponent
                :avatar-index="request.avatar"
                :name="request.userName"
                variant="acceptReject"
                @accept="
                  handleFriendAction('accept', request.userId, false, index, request.friendship_id)
                "
                @reject="
                  handleFriendAction('reject', request.userId, false, index, request.friendship_id)
                "
              />
            </v-col>
          </v-row>
        </v-sheet>

        <!-- Outgoing Requests -->
        <v-sheet v-if="currentSubpage === 'outgoing'">
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
            <v-col v-for="(request, index) in outgoingRequests" :key="request.userId" cols="12">
              <FriendComponent
                :avatar-index="request.avatar"
                :name="request.userName"
                variant="dismiss"
                @dismiss="
                  handleFriendAction('dismiss', request.userId, false, index, request.friendship_id)
                "
              />
            </v-col>
          </v-row>
        </v-sheet>
      </div>

      <!-- Search Results -->
      <div v-else>
        <!-- Existing Friends Section -->
        <div
          v-if="searchResults.filter((result) => result.status === 'You are friends.').length > 0"
        >
          <h3 class="section-title2 text-primaryBlue">
            Existing Friends -
            {{ searchResults.filter((result) => result.status === 'You are friends.').length }}
          </h3>
          <v-row class="friend-scroll">
            <v-col
              v-for="result in searchResults.filter(
                (result) => result.status === 'You are friends.',
              )"
              :key="result.user_data.user_id"
              cols="12"
            >
              <FriendComponent
                :avatar-index="result.user_data.avatar"
                :name="result.user_data.username"
                variant="details"
              />
            </v-col>
          </v-row>
        </div>

        <!-- Other Users Section -->
        <div
          v-if="searchResults.filter((result) => result.status !== 'You are friends.').length > 0"
        >
          <h3 class="section-title2 text-primaryBlue">
            Other Users -
            {{ searchResults.filter((result) => result.status !== 'You are friends.').length }}
          </h3>
          <v-row class="friend-scroll">
            <v-col
              v-for="(result, index) in searchResults.filter(
                (result) => result.status !== 'You are friends.',
              )"
              :key="result.user_data.user_id"
              cols="12"
            >
              <FriendComponent
                :avatar-index="result.user_data.avatar"
                :name="result.user_data.username"
                :variant="getUserVariant(result.status)"
                @send="handleFriendAction('send', result.user_data.user_id, true, index, undefined)"
                @accept="
                  handleFriendAction(
                    'accept',
                    result.user_data.user_id,
                    true,
                    index,
                    result.friendship_id,
                  )
                "
                @reject="
                  result.friendship_id &&
                    handleFriendAction(
                      'reject',
                      result.user_data.user_id,
                      true,
                      index,
                      result.friendship_id,
                    )
                "
                @dismiss="
                  result.friendship_id &&
                    handleFriendAction(
                      'dismiss',
                      result.user_data.user_id,
                      true,
                      index,
                      result.friendship_id,
                    )
                "
              />
            </v-col>
          </v-row>
        </div>

        <!-- No Results Message -->
        <template v-if="searchQuery && searchResults.length === 0">
          <div v-if="searchResultsLoading" class="d-flex w-100 justify-center">
            <v-progress-circular indeterminate color="primaryBlue" />
          </div>

          <div v-else class="text-center my-6">
            <p class="text-primaryBlue font-italic">
              No users found matching "{{ searchQuery }}" <br />Try a different search term
            </p>
          </div>
        </template>
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

.search-field {
  max-width: 100%;
}

.font-poppins {
  font-family: 'Poppins', cursive !important;
  font-weight: bold !important;
}
</style>
