<template>
    <v-dialog v-model="dialog" max-width="400px" persistent>
      <template v-slot:activator="{ on, attrs }">
        <v-btn color="primary" dark v-bind="attrs" v-on="on">Login</v-btn>
      </template>

      <v-card>
        <v-card-title class="d-flex justify-center">
          <img src="@/assets/logo.png" alt="Blue Crew Logo" style="width: 100px;" />
        </v-card-title>
        <v-card-subtitle class="text-center text-h6 mt-2">
          Welcome Back
        </v-card-subtitle>
        <v-card-text>
          <p class="text-center mb-4">Login to your existing account</p>

          <v-form ref="form" v-model="valid" lazy-validation>
            <v-text-field
              v-model="username"
              label="Username"
              required
              outlined
              dense
            ></v-text-field>

            <v-text-field
              v-model="password"
              label="Password"
              type="password"
              required
              outlined
              dense
            ></v-text-field>

            <v-btn text class="mt-2" @click="forgotPassword">
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
  .text-h6 {
    font-weight: bold;
    color: #8a2be2; /* Customize color */
  }

  a {
    color: #ff4081;
    text-decoration: none;
  }

  a:hover {
    text-decoration: underline;
  }
  </style>