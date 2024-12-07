<template>
    <v-dialog v-model="dialog" max-width="400px">
      <template v-slot:activator="{props: activatorProps }">
        <v-btn
            v-bind="activatorProps"
            text = "Login"></v-btn>
      </template>

      <v-card>
        <v-container>
            <v-row> 
                <v-spacer />
                <v-icon icon="mdi-close-circle-outline" class="mr-3 mt-3"></v-icon>
            </v-row>
        </v-container>

        <v-card-title class="d-flex justify-center">
          <img src="@/assets/bluecrew-logo.png" alt="Blue Crew Logo" style="width: 100px;" />
        </v-card-title>

        
        <v-card-subtitle class="text-center subtitle mt-2">
          Welcome Back
        </v-card-subtitle>
        <v-card-text>
          <p class="text-center mb-4">Login to your existing account</p>

          <v-form v-model="valid" lazy-validation>
            <v-card-subtitle class="text-left subtitle mb-3 pa-0 text-primaryPink">
              Username
            </v-card-subtitle>
            <v-text-field
              v-model="username"
              label="Enter your username"
              required
              outlined
            ></v-text-field>

            <v-card-subtitle class="text-left subtitle  mb-3 pa-0 text-primaryPink">
              Password
            </v-card-subtitle>
            <v-text-field
              v-model="password"
              label="Enter your password"
              type="password"
              required
              outlined
            ></v-text-field>

            <v-btn class="mt-2" @click="forgotPassword">
              Forgot Password?
            </v-btn>

            <v-btn
              class="mt-4"
              color="primary"
              block
              :disabled="!valid"
              @click="login"
            >
              Sign In
            </v-btn>
          </v-form>
        </v-card-text>

        <v-card-actions class="d-flex justify-center">
          <p>Don't have an account? <a href="/signup">Sign up</a></p>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>

  <script lang="ts">
    import { defineComponent, ref } from "vue";
    export default defineComponent({
        name: "LoginModal",
        setup() {
        const dialog = ref(false);
        const username = ref("");
        const password = ref("");
        const valid = ref(false);

        const login = () => {
            // Implement login logic here
            console.log("Logging in with:", { username: username.value, password: password.value });
        };

        const forgotPassword = () => {
            // Implement forgot password functionality
            console.log("Forgot password clicked");
        };

        return {
            dialog,
            username,
            password,
            valid,
            login,
            forgotPassword,
        };
        },
    });
  </script>

  <style scoped>
  .subtitle {
    font-weight: bold;
    opacity: 1;
  }

  a {
    color: #ff4081;
    text-decoration: none;
  }

  a:hover {
    text-decoration: underline;
  }
  </style>