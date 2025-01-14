<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  avatarIndex: number
  name: string
  variant?: 'default' | 'acceptReject' | 'dismiss' | 'delete' | 'addFriend' | 'accept'
}>()

const showDialog = ref(false)

const emit = defineEmits(['accept', 'reject', 'dismiss', 'delete', 'addFriend'])
</script>

<template>
  <div class="friend-row">
    <v-img
      class="rounded-circle"
      max-height="32"
      max-width="32"
      min-width="32"
      cover
      src="https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg"
    ></v-img>
    <v-text class="me-auto font-weight-bold truncate-name">{{ name }}</v-text>

    <!-- Accept/Reject variant -->
    <div v-if="variant === 'acceptReject'" class="acceptreject">
      <v-icon icon="mdi-check" @click="emit('accept')" class="cursor-pointer" />
      <v-icon icon="mdi-close" @click="emit('reject')" class="cursor-pointer" />
    </div>

    <!-- Dismiss variant -->
    <div v-if="variant === 'dismiss'" class="dismiss-action">
      <v-btn color="primaryBlue" variant="flat" @click="emit('dismiss')" class="dismiss-btn">
        Dismiss
      </v-btn>
    </div>

    <!-- Delete variant -->
    <div v-if="variant === 'delete'" class="delete-action">
      <v-btn color="primaryPink" variant="flat" @click="showDialog = true"> Delete </v-btn>

      <!-- Delete confirmation dialog -->
      <v-dialog v-model="showDialog" max-width="400">
        <v-card>
          <strong>Confirm Deletion</strong>
          <p>Are you sure you want to delete this friend?</p>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primaryBlue" variant="flat" @click="showDialog = false"> Cancel </v-btn>
            <v-btn color="primaryPink" variant="flat" @click="emit('delete'), (showDialog = false)">
              Confirm
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>

    <!-- Add Friend variant -->
    <div v-if="variant === 'addFriend'" class="add-friend-action">
      <v-btn color="primaryPink" variant="flat" @click="emit('addFriend')"> Add Friend </v-btn>
    </div>

    <!-- Accept variant -->
    <div v-if="variant === 'accept'" class="accept-action">
      <v-btn color="primaryPink" variant="flat" @click="emit('accept')"> Accept </v-btn>
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
.accept-action {
  margin-left: 8px;
}

.cursor-pointer {
  cursor: pointer;
}
</style>
