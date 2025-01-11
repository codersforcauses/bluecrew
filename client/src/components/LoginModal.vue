<script setup lang="ts">
import { ref, computed } from 'vue'
import { useModalStore } from '@/stores/modal'
import { useDisplay } from 'vuetify'

const { xs } = useDisplay()
const modalStore = useModalStore()

const isDialogVisible = computed({
  get: () => modalStore.currentModal === 'login',
  set: (value: boolean) => {
    if (!value) {
      modalStore.closeModal()
    }
  },
})

const closeDialog = () => {
  modalStore.closeModal()
}

const openRegisterModal = () => {
  modalStore.openRegister()
}

const username = ref('')
const password = ref('')
const valid = ref(false)
</script>

<template>
  <v-dialog
    v-model="isDialogVisible"
    :max-width="xs ? '100%' : '400px'"
    :fullscreen="xs"
    scrollable
    persistent
  >
    <v-card>
      <v-container>
        <v-row>
          <v-spacer />
          <button class="close-button" @click="closeDialog">
            <v-icon icon="mdi-close-circle-outline" class="mr-3 mt-3"></v-icon>
          </button>
        </v-row>
      </v-container>

      <v-card-title class="d-flex justify-center">
        <img src="@/assets/bluecrew-logo.png" alt="Blue Crew Logo" style="width: 100px" />
      </v-card-title>

      <v-card-subtitle class="text-center subtitle mt-2 text-primaryPink">
      <strong><h3><b>Welcome Back</b></h3></strong>
      </v-card-subtitle>
      <v-card-text>
        <p class="text-center subtitle mb-4 text-primaryPink">
          <b>Login to your existing account</b>
        </p>

        <v-form v-model="valid" lazy-validation>
          <v-card-subtitle class="text-left subtitle mb-3 pa-0 text-primaryPink" style="font-family: 'poppins'; font-size: 16px; font-weight: bold;" >
            Username
          </v-card-subtitle>
          <v-text-field
            v-model="username"
            placeholder="Enter your username"
            hide-details="auto"
            required
            outlined
            class="bg-primaryBrown"
            variant="outlined"
          ></v-text-field>

          <v-card-subtitle class="text-left subtitle mt-3 mb-3 pa-0 text-primaryPink" style="font-family: 'poppins'; font-size: 16px; font-weight: bold;" >
            Password
          </v-card-subtitle>
          <v-text-field
            v-model="password"
            placeholder="Enter your password"
            hide-details="auto"
            type="password"
            required
            outlined
            hide-detials
            class="bg-primaryBrown"
            variant="outlined"
          ></v-text-field>

          <div class="mt-3">
            <a href="/forgot-password" class="text-lightBlue">
              <b class="text-subtitle-2"><forgotpass>Forgot Password?</forgotpass></b>
            </a>
          </div>
          <v-btn
            class="d-flex justify-center mt-4 w-50 mx-auto"
            color="primaryBlue"
            :style="{ height: '50px' }"
            :disabled="!valid"
            rounded
            elevation="12"
          >
            Sign In
          </v-btn>
        </v-form>
      </v-card-text>

      <v-card-actions class="d-flex justify-center text-primaryPink">
        <footer>
          Don't have an account? <a href="#" class="text-primaryPink" @click.prevent="openRegisterModal">Sign up</a>
        </footer>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.subtitle {
  font-weight: bold;
  opacity: 1;
}

a:hover {
  text-decoration: underline;
}

.close-button {
  width: 30px;
  height: 30px;
  display: flex;
  align-self: flex-end;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  background: none;
  color: black;
  border: 3px;
  border-color: black;
  cursor: pointer;
  padding: 0;
}

strong {
  width: 100%;
  display: flex;
  flex-direction: column;
  font-size: 19px;
  font-family: poppins;
  margin-bottom: 0px;
  align-items: center;
}

p {
  width: 100%;
  display: flex;
  flex-direction: column;
  font-size: 18px;
  font-family: poppins;
  margin-bottom: 10px;
  align-items: center;
  font-weight: bold;
}

forgotpass {
  font-family: poppins;
  font-weight: bold;
}

footer {
  text-align: center;
  font-family: poppins;
  font-weight: bold;
}

</style>
