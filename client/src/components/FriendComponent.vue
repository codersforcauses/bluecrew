<script setup lang="ts">
import { ref } from 'vue'
import avatarPaths from '@/utils/avatar'
import { navigateToProfile } from '@/router'

defineProps<{
  avatarIndex: number
  name: string
  variant?:
    | 'default'
    | 'acceptReject'
    | 'dismiss'
    | 'delete'
    | 'addFriend'
    | 'accept'
    | 'details'
    | 'send'
    | 'requestSent'
}>()

const showDialog = ref(false)
const emit = defineEmits(['accept', 'reject', 'dismiss', 'delete', 'addFriend', 'details', 'send'])

const handleUsernameClick = (username: string) => {
  navigateToProfile(username)
}
</script>

<template>
  <div class="friend-row">
    <v-img
      class="rounded-circle"
      max-height="32"
      max-width="32"
      min-width="32"
      cover
      :src="`/${avatarPaths[avatarIndex]}`"
    />
    <p
      class="me-auto font-weight-bold truncate-name username-link"
      @click="handleUsernameClick(name)"
    >
      {{ name }}
    </p>

    <!-- Accept/Reject variant -->
    <div v-if="variant === 'acceptReject'" class="acceptreject">
      <v-icon icon="mdi-check" @click="emit('accept')" class="cursor-pointer" />
      <v-icon icon="mdi-close" @click="emit('reject')" class="cursor-pointer" />
    </div>

    <!-- Dismiss variant -->
    <div v-if="variant === 'dismiss'" class="dismiss-action">
      <v-btn color="primaryBlue" variant="flat" @click="emit('dismiss')" class="font-poppins">
        Dismiss
      </v-btn>
    </div>

    <!-- Delete variant -->
    <div v-if="variant === 'delete'" class="delete-action">
      <v-btn color="primaryGreen" variant="flat" @click="showDialog = true" class="font-poppins">
        Delete
      </v-btn>

      <!-- Delete confirmation dialog -->
      <v-dialog v-model="showDialog" max-width="400">
        <v-card>
          <strong>Confirm Deletion</strong>
          <p>Are you sure you want to delete this friend?</p>
          <v-card-actions>
            <v-spacer />
            <v-btn
              color="primaryBlue"
              variant="flat"
              @click="showDialog = false"
              class="font-poppins"
            >
              Cancel
            </v-btn>
            <v-btn
              color="primaryGreen"
              variant="flat"
              @click="emit('delete'), (showDialog = false)"
              class="font-poppins"
            >
              Confirm
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>

    <!-- Send variant -->
    <div v-if="variant === 'send'" class="send-action">
      <v-btn color="primaryBlue" variant="flat" @click="emit('send')" class="font-poppins">
        Send
      </v-btn>
    </div>

    <!-- Request Sent variant -->
    <div v-if="variant === 'requestSent'" class="request-sent-action">
      <v-btn color="primaryBlue" variant="flat" disabled class="opacity-75 font-poppins">
        Request Sent
      </v-btn>
    </div>

    <!-- Add Friend variant -->
    <div v-if="variant === 'addFriend'" class="add-friend-action">
      <v-btn color="primaryGreen" variant="flat" @click="emit('addFriend')" class="font-poppins">
        Add Friend
      </v-btn>
    </div>

    <!-- Accept variant -->
    <div v-if="variant === 'accept'" class="accept-action">
      <v-btn color="primaryGreen" variant="flat" @click="emit('accept')" class="font-poppins">
        Accept
      </v-btn>
    </div>
  </div>
</template>

<style scoped>
strong {
  font-weight: bold;
  font-family: poppins;
  font-size: 24px;
  color: rgb(var(--v-theme-primaryGrey));
  padding: 10px;
}

p {
  font-weight: bold;
  font-family: poppins;
  color: rgb(var(--v-theme-primaryGrey));
  padding: 10px;
}

.friend-row {
  display: flex;
  gap: 16px;
  min-height: 50px;
  padding-left: 20px;
  padding-right: 20px;
  border: 1px solid;
  align-items: center;
  border-radius: 8px;
  background-color: rgb(var(--v-theme-creamWhite));
  border-color: rgb(var(--v-theme-primaryBlue));
  color: rgb(var(--v-theme-primaryGrey));
}

.truncate-name {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.acceptreject {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-right: 8px;
}

.dismiss-action,
.delete-action,
.add-friend-action,
.accept-action,
.details-action,
.send-action,
.request-sent-action {
  margin-left: 8px;
}

.cursor-pointer {
  cursor: pointer;
}

.font-poppins {
  font-family: 'Poppins', cursive !important;
  font-weight: bold !important;
}

.username-link {
  cursor: pointer;
  &:hover {
    text-decoration: underline;
    color: rgb(var(--v-theme-primaryBlue));
  }
}
</style>
