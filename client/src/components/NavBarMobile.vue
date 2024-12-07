<template>
    <div class="mobile-nav">
        <!-- Only hamburger button when menu is closed -->
        <div v-if="!isMenuOpen" class="menu-trigger">
            <div class="menu-icon" @click="toggleMenu">
                <van-icon name="bars" color="#FF1493" size="28" />
            </div>
        </div>

        <!-- Navigation menu popup with header -->
        <van-popup v-model:show="isMenuOpen" position="top" :overlay="true" class="menu-popup">
            <!-- Header bar that appears with menu -->
            <div class="nav-header">
                <div class="header-content">
                    <img src="@/assets/logo.png" alt="Blue Crew Logo" class="logo">
                    <div class="username">Guest Mode</div>
                    <div class="menu-icon" @click="toggleMenu">
                        <van-icon name="bars" color="#FF1493" size="28" />
                    </div>
                </div>
            </div>

            <div class="menu-content">
                <!-- Navigation buttons -->
                <div class="menu-items">
                    <button class="menu-button">
                        <span class="button-text">Home</span>
                    </button>

                    <button class="menu-button disabled">
                        <van-icon name="lock" class="lock-icon" />
                        <span class="button-text">User Preferences</span>
                    </button>

                    <button class="menu-button disabled">
                        <van-icon name="lock" class="lock-icon" />
                        <span class="button-text">Friends</span>
                    </button>

                    <button class="menu-button">
                        <span class="button-text">Leaderboard</span>
                    </button>
                </div>

                <!-- Authentication section -->
                <div class="auth-section">
                    <button class="sign-in-button" @click="handleAuth">
                        Sign In
                    </button>

                    <div class="signup-hint">
                        Don't have an account?
                        <router-link to="/signup" class="signup-link">Sign up</router-link>
                    </div>
                </div>
            </div>
        </van-popup>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { Icon as VanIcon, Popup as VanPopup } from 'vant'

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

/* Initial menu trigger button styles */
.menu-trigger {
    position: fixed;
    top: 16px;
    right: 16px;
    z-index: 1000;
}

/* Header styles */
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

.menu-icon {
    background-color: white;
    padding: 8px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}

/* Menu popup styles */
.menu-popup {
    background-color: #193855;
}

.menu-content {
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

/* Navigation buttons styles */
.menu-items {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.menu-button {
    width: 100%;
    background-color: rgba(233, 218, 196, 0.8);
    border: none;
    border-radius: 12px;
    padding: 14px;
    position: relative;
    min-height: 54px;
    font-family: 'Poppins', 'Arial', sans-serif;
    font-size: 24px;
    font-weight: 900;
}

.button-text {
    width: 100%;
    text-align: center;
    display: block;
}

.menu-button.disabled {
    opacity: 0.8;
    background-color: #A9A9A9;
}

.lock-icon {
    position: absolute;
    left: 20px;
    top: 50%;
    transform: translateY(-50%);
}

/* Authentication section styles */
.auth-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    margin-top: 8px;
}

.sign-in-button {
    width: 200px;
    background-color: transparent;
    color: white;
    border: 2px solid white;
    border-radius: 25px;
    padding: 12px 24px;
    font-size: 20px;
    font-weight: 900;
    cursor: pointer;
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

/* Vant component overrides */
:deep(.van-popup) {
    background-color: #193855 !important;
}
</style>
