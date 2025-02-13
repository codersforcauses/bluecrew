<template>
  <div class="mobile-nav">
    <div v-if="!isMenuOpen" class="menu-trigger">
      <v-btn icon @click="toggleMenu" class="menu-icon text-primaryWhite">
        <v-icon class="text-primaryGreen" size="28">mdi-menu</v-icon>
      </v-btn>
    </div>

    <v-navigation-drawer
      v-model="isMenuOpen"
      location="top"
      temporary
      class="menu-drawer bg-primaryBlue"
      width="100%"
    >
      <div class="menu-header">
        <span class="guest-mode text-primaryWhite">{{ userName || 'Guest Mode' }}</span>
        <v-btn icon @click="toggleMenu" class="menu-icon fixed-position">
          <v-icon class="text-primaryGreen" size="28">mdi-menu</v-icon>
        </v-btn>
      </div>

      <div class="menu-content">
        <div class="menu-items">
          <v-btn
            v-for="(page, index) in pages"
            :key="index"
            block
            class="menu-button bg-creamWhite"
            variant="text"
            height="64"
            @click="navigate(page.routerName)"
            :style="{ opacity: !page.requireAuth || isLoggedIn ? 1 : 0.5 }"
          >
            <span class="button-text text-primaryGrey">{{ page.name }}</span>
          </v-btn>
        </div>

        <div class="auth-section">
          <div v-if="!isLoggedIn" class="sign-in-buttons">
            <v-btn
              class="sign-in-button text-primaryWhite"
              rounded
              @click="$emit('sign-in-click', 'login')"
            >
              Sign In
            </v-btn>

            <p class="signup-hint text-primaryWhite" @click="$emit('sign-in-click', 'register')">
              Don't have an account?
              <span class="signup-link text-primaryWhite">Please register</span>
            </p>
          </div>

          <div v-else>
            <v-btn class="sign-in-button text-primaryWhite" rounded @click="auth"> Sign Out </v-btn>
          </div>
        </div>
      </div>
    </v-navigation-drawer>
  </div>
</template>

<script setup lang="ts">
import type { NavigationInfo } from '@/types/navigation'
import { ref } from 'vue'

defineProps<{
  isLoggedIn: boolean
  userName: string
  pages: NavigationInfo[]
}>()

const emit = defineEmits(['navigate', 'auth', 'sign-in-click'])

const isMenuOpen = ref(false)
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const navigate = (route: string) => {
  emit('navigate', route)
  isMenuOpen.value = false
}

const auth = () => {
  emit('auth')
  isMenuOpen.value = false
}
</script>

<style scoped>
.mobile-nav {
  width: 100%;
}

.menu-trigger {
  position: fixed;
  top: 0;
  right: 0;
  z-index: 999;
}

.menu-icon {
  border-radius: 8px;
}

.fixed-position {
  position: fixed;
  top: 0;
  right: 0px;
  z-index: 999;
}

.menu-drawer {
  padding-top: 16px;
  min-height: 490px;
}

.menu-header {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 16px;
  margin-bottom: 24px;
}

.guest-mode {
  font-family: 'Lilita One', Arial, sans-serif;
  font-size: 24px;
  font-weight: 400;
  text-align: center;
}

.menu-content {
  padding: 0 16px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.menu-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.menu-button {
  border-radius: 16px;
  font-family: 'Poppins', Arial, sans-serif;
  font-size: 20px;
  font-weight: 900;
  text-transform: none;
  position: relative;
  letter-spacing: 0;
  opacity: 0.8;
  height: 56px;
}

.button-text {
  width: 100%;
  text-align: center;
  font-weight: 900 !important;
}

.auth-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 8px;
  padding-bottom: 8px;
}

.sign-in-buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.sign-in-button {
  width: 160px;
  background-color: transparent;
  border: 2px solid white;
  border-radius: 30px;
  height: 48px;
  font-family: 'Lilita One', Arial, sans-serif;
  font-size: 24px;
  font-weight: 400;
  text-transform: none;
  letter-spacing: 0;
}

.signup-hint {
  font-size: 16px;
  font-weight: 500;
  text-align: center;
  margin-top: 8px;
  cursor: pointer;
}

.signup-link {
  text-decoration: underline;
  font-weight: 500;
}
</style>
