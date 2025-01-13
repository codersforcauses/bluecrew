<script setup lang="ts">
import { ref } from 'vue';

defineProps<{
  avatarIndex: number
  name: string
  variant?: 'default' | 'acceptReject' | 'dismiss' | 'delete' | 'addFriend' | 'accept'
}>();

const showDialog = ref(false);

const emit = defineEmits(['accept', 'reject', 'dismiss', 'delete', 'addFriend']);
</script>

<template>
  <v-col class="rounded-lg d-flex ga-3 px-5 outline align-center bg-creamWhite text-primaryGrey">
    <v-img
      class="rounded-circle"
      max-height="32"
      max-width="32"
      min-width="32"
      cover
      src="https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg"
    ></v-img>
    <v-text class="me-auto font-weight-bold truncate-name">{{ name }}</v-text>
    
    <!-- Default slot-->
    <slot name="default"></slot>

    <!-- Accept/Reject variant -->
    <div v-if="variant === 'acceptReject'" class="acceptreject">
      <slot name="acceptreject">
        <v-icon 
          icon="mdi-check" 
          @click="emit('accept')"
          class="cursor-pointer"
        />
        <v-icon 
          icon="mdi-close" 
          @click="emit('reject')"
          class="cursor-pointer"
        />
      </slot>
    </div>

    <!-- Dismiss variant -->
    <div v-if="variant === 'dismiss'" class="dismiss-action">
      <slot name="dismiss">
        <v-btn
          color="primaryBlue"
          variant="flat"
          @click="emit('dismiss')"
          class="dismiss-btn"
        >
          Dismiss
        </v-btn>
      </slot>
    </div>

    <!-- Delete variant -->
    <div v-if="variant === 'delete'" class="delete-action">
      <slot name="delete">
        <v-btn
          color="primaryPink"
          variant="flat"
          @click="showDialog = true"
        >
          Delete
        </v-btn>
      </slot>

      <!-- Delete confirmation dialog -->
      <v-dialog v-model="showDialog" max-width="400">
        <v-card>
          <v-card-title>Confirm Deletion</v-card-title>
          <v-card-text>Are you sure you want to delete this friend?</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primaryBlue" variant="flat" @click="showDialog = false">
              Cancel
            </v-btn>
            <v-btn color="primaryPink" variant="flat"  @click="emit('delete'); showDialog = false">
              Confirm
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>

    <!-- Add Friend variant -->
    <div v-if="variant === 'addFriend'" class="add-friend-action">
      <slot name="addfriend">
        <v-btn
          color="primaryPink"
          variant="flat"
          @click="emit('addFriend')"
        >
          Add Friend
        </v-btn>
      </slot>
    </div>

    <!-- Accept variant -->
    <div v-if="variant === 'accept'" class="accept-action">
      <slot name="accept">
        <v-btn
          color="primaryPink"
          variant="flat"
          @click="emit('accept')"
        >
          Accept
        </v-btn>
      </slot>
    </div>
  </v-col>
</template>

<style scoped>
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