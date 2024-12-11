<template>
    <div class="mobile-nav">
        <!-- Only hamburger button when menu is closed -->
        <div v-if="!isMenuOpen" class="menu-trigger">
            <v-btn icon @click="toggleMenu" class="menu-icon">
                <v-icon color="#FF1493" size="28">mdi-menu</v-icon>
            </v-btn>
        </div>

        <!-- Navigation menu drawer with header -->
        <v-navigation-drawer v-model="isMenuOpen" location="top" temporary class="menu-drawer">
            <!-- Header bar that appears with menu -->
            <div class="nav-header">
                <div class="header-content">
                    <!-- don't need the logo now -->
                    <!-- <img src="@/assets/logo.png" alt="Blue Crew Logo" class="logo"> -->
                    <div class="username">Guest Mode</div>
                    <v-btn icon @click="toggleMenu" class="menu-icon">
                        <v-icon color="#FF1493" size="28">mdi-menu</v-icon>
                    </v-btn>
                </div>
            </div>

            <div class="menu-content">
                <!-- Navigation buttons -->
                <div class="menu-items">
                    <v-btn block class="menu-button" variant="text" height="54">
                        Home
                    </v-btn>

                    <v-btn block class="menu-button disabled" variant="text" height="54" disabled>
                        <v-icon class="lock-icon">mdi-lock</v-icon>
                        <span class="button-text">User Preferences</span>
                    </v-btn>

                    <v-btn block class="menu-button disabled" variant="text" height="54" disabled>
                        <v-icon class="lock-icon">mdi-lock</v-icon>
                        <span class="button-text">Friends</span>
                    </v-btn>

                    <v-btn block class="menu-button" variant="text" height="54">
                        Leaderboard
                    </v-btn>
                </div>

                <!-- Authentication section -->
                <div class="auth-section">
                    <v-btn class="sign-in-button" outlined @click="handleAuth">
                        Sign In
                    </v-btn>

                    <div class="signup-hint">
                        Don't have an account?
                        <router-link to="/signup" class="signup-link">Sign up</router-link>
                    </div>
                </div>
            </div>
        </v-navigation-drawer>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// State management
const isMenuOpen = ref(false)
const isLoggedIn = ref(false)

// Methods
const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value
}

const handleAuth = () => {
    if (isLoggedIn.value) {
        isLoggedIn.value = false
    } else {
        // Handle login logic
    }
}
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

.nav-header {
    background-color: #193855;
    padding: 12px 16px;
    width: 100%;
}

.header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    max-width: 480px;
    margin: 0 auto;
}

.logo {
    height: 40px;
    width: 40px;
    object-fit: contain;
}

.username {
    color: white;
    font-family: 'Lilita One', 'Arial Black', sans-serif;
    font-size: 24px;
    text-align: center;
    flex-grow: 1;
}

.menu-drawer {
    background-color: #193855 !important;
}

.menu-content {
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.menu-items {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.menu-button {
    background-color: rgba(233, 218, 196, 0.8) !important;
    border-radius: 12px !important;
    font-family: 'Poppins', 'Arial', sans-serif !important;
    font-size: 24px !important;
    font-weight: 900 !important;
    text-transform: none !important;
    position: relative;
}

.menu-button.disabled {
    background-color: #A9A9A9 !important;
    opacity: 0.8 !important;
}

.button-text {
    width: 100%;
    text-align: center;
}

.lock-icon {
    position: absolute;
    left: 20px;
}

.auth-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    margin-top: 8px;
}

.sign-in-button {
    width: 200px !important;
    background-color: transparent !important;
    color: white !important;
    border: 2px solid white !important;
    border-radius: 25px !important;
    padding: 12px 24px !important;
    font-size: 20px !important;
    font-weight: 900 !important;
    text-transform: none !important;
}

.signup-hint {
    color: white;
    font-size: 16px;
    font-weight: 700;
    text-align: center;
}

.signup-link {
    color: white;
    text-decoration: underline;
    font-weight: 700;
}
</style>