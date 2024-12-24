<script setup lang="ts">
import { ref, computed, watch, onMounted, nextTick } from 'vue';
import { useDisplay } from 'vuetify';
import { useRouter } from 'vue-router';
import NavBarMobile from '@/components/NavBarMobile.vue';
import NavBarDesktop from '@/components/NavBarDesktop.vue';
import { useUserStore } from '@/stores/user';
import { useModalStore } from '@/stores/modal';

const userStore = useUserStore();
const modalStore = useModalStore();
const { smAndUp } = useDisplay();
const router = useRouter();

// Dynamically Calculate the height of NavBar
const navBarHeight = ref(0);
const updateNavBarHeight = async () => {
  await nextTick();
  const navBarSelector = smAndUp.value ? '.nav-bar-desktop' : '.nav-bar-mobile';
  const navBarElement = document.querySelector(navBarSelector);
  if (navBarElement) {
    navBarHeight.value = navBarElement.clientHeight;
  }
};

onMounted(() => {
  updateNavBarHeight();
  watch(smAndUp, () => {
    updateNavBarHeight();
  });
});

// Logging in Status
const isLoggedIn = computed(() => userStore.isLoggedIn);
const userName = computed(() => userStore.userData?.userName || '');
const truncatedUserName = computed(() => {
  return userName.value.length > 10 ? `${userName.value.slice(0, 10)}...` : userName.value;
});

// Event Handling 
const handleAuth = async () => {
  if (isLoggedIn.value) {
    await userStore.logout();
  } else {
    modalStore.openLogin();
  }
};

const handleNavigation = (page: string) => {
  if (!isLoggedIn.value && ['friends', 'preferences'].includes(page)) {
    alert('You must be logged in to access this page.');
    return;
  }
  router.push({ name: page });
};

defineExpose({
  navBarHeight,
});

export type NavBarWrapperExpose = {
  navBarHeight: number;
};
</script>

<template>
  <div>
    <!-- Desktop Version -->
    <div v-if="smAndUp" class="nav-bar-desktop">
      <NavBarDesktop
        :is-logged-in="isLoggedIn"
        :user-name="truncatedUserName"
        @navigate="handleNavigation"
        @auth="handleAuth"
      />
    </div>

    <!-- Mobile Version -->
    <div v-else class="nav-bar-mobile">
      <NavBarMobile
        :is-logged-in="isLoggedIn"
        :user-name="truncatedUserName"
        @navigate="handleNavigation"
        @auth="handleAuth"
      />
    </div>
  </div>
</template>

<style scoped>
.nav-bar-desktop {
  height: 48px;
}

.nav-bar-mobile {
  height: 16px;
}
</style>
