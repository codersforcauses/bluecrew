<template>
  <div class="mobile-nav">
    <div v-if="!isMenuOpen" class="menu-trigger">
      <v-btn icon @click="toggleMenu" class="menu-icon">
        <v-icon color="#FF1493" size="28">mdi-menu</v-icon>
      </v-btn>
    </div>

    <v-navigation-drawer
      v-model="isMenuOpen"
      location="top"
      temporary
      class="menu-drawer"
      width="100%"
    >
      <div class="menu-header">
        <span class="guest-mode">{{ userName || 'Guest Mode' }}</span>
        <v-btn icon @click="toggleMenu" class="menu-icon fixed-position">
          <v-icon color="#FF1493" size="28">mdi-menu</v-icon>
        </v-btn>
      </div>

      <div class="menu-content">
        <div class="menu-items">
          <v-btn block class="menu-button" variant="text" height="64" @click="navigate('home')">
            <span class="button-text">Home</span>
          </v-btn>

          <v-btn
            block
            class="menu-button"
            :class="{ disabled: !isLoggedIn }"
            variant="text"
            height="64"
            :disabled="!isLoggedIn"
            @click="navigate('user-preferences')"
          >
            <v-icon v-if="!isLoggedIn" class="lock-icon" size="24">mdi-lock</v-icon>
            <span class="button-text">User Preferences</span>
          </v-btn>

          <v-btn
            block
            class="menu-button"
            :class="{ disabled: !isLoggedIn }"
            variant="text"
            height="64"
            :disabled="!isLoggedIn"
            @click="navigate('friends')"
          >
            <v-icon v-if="!isLoggedIn" class="lock-icon" size="24">mdi-lock</v-icon>
            <span class="button-text">Friends</span>
          </v-btn>

          <v-btn block class="menu-button" variant="text" height="64" @click="navigate('leaderboard')">
            <span class="button-text">Leaderboard</span>
          </v-btn>
        </div>

        <div class="auth-section">
          <v-btn class="sign-in-button" rounded @click="auth">
            {{ isLoggedIn ? 'Log Out' : 'Sign In' }}
          </v-btn>
        </div>
      </div>
    </v-navigation-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue';

defineProps({
  isLoggedIn: Boolean,
  userName: String,
});

const emit = defineEmits(['navigate', 'auth']);

const isMenuOpen = ref(false);
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

const navigate = (route: string) => {
  emit('navigate', route);
  isMenuOpen.value = false;
};

const auth = () => {
  emit('auth');
  isMenuOpen.value = false;
};
</script>

<style scoped>
.mobile-nav {
  width: 100%;
}

.menu-trigger {
  position: fixed;
  top: 16px;
  right: 16px;
  z-index: 1000;
}

.menu-icon {
  background-color: white !important;
  border-radius: 8px !important;
}

.fixed-position {
  position: fixed !important;
  top: 16px !important;
  right: 16px !important;
  z-index: 1000;
}

.menu-drawer {
  background-color: #193855 !important;
  padding-top: 16px !important;
  min-height: 490px !important;
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
  color: white;
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
  background-color: #e9dac4 !important;
  border-radius: 16px !important;
  font-family: 'Poppins', Arial, sans-serif !important;
  font-size: 20px !important;
  font-weight: 900 !important;
  text-transform: none !important;
  position: relative;
  letter-spacing: 0 !important;
  opacity: 0.8;
  height: 56px !important;
}

.menu-button.disabled {
  background-color: #a9a9a9 !important;
  opacity: 0.8 !important;
}

.button-text {
  width: 100%;
  text-align: center;
  font-weight: 900 !important;
}

.lock-icon {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
}

.auth-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-top: 16px;
  padding-bottom: 4px;
}

.sign-in-button {
  width: 160px !important;
  background-color: transparent !important;
  color: white !important;
  border: 2px solid white !important;
  border-radius: 30px !important;
  height: 48px !important;
  font-family: 'Lilita One', Arial, sans-serif !important;
  font-size: 24px !important;
  font-weight: 400 !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
}

.signup-hint {
  color: white;
  font-size: 16px;
  font-weight: 500;
  text-align: center;
}

.signup-link {
  color: white;
  text-decoration: underline;
  font-weight: 500;
}
</style>
