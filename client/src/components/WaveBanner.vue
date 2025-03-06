<template>
  <div class="wave-banner-wrapper">
    <div class="wave-banner">
      <!-- Header Image -->
      <v-img :src="imageSrc" :alt="altText" class="header-image" cover />

      <!-- Custom Wave Shape -->
      <div class="custom-shape-divider-bottom-1736569822">
        <svg
          data-name="Layer 1"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 1200 120"
          preserveAspectRatio="none"
        >
          <path
            d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z"
            class="shape-fill"
          />
        </svg>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps({
  imageSrc: {
    type: String,
    required: true,
  },
  altText: {
    type: String,
    required: false,
    default: 'Banner image',
  },
})
</script>

<style scoped>
.wave-banner-wrapper {
  position: relative;
  width: 100vw;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
  min-width: 300px;
  overflow: hidden;
}

.wave-banner {
  position: relative;
  width: 100%;
  height: 200px;
  margin-bottom: 15px;
}

.header-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.custom-shape-divider-bottom-1736569822 {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  overflow: hidden;
  line-height: 0;
  transform: rotate(180deg);
}

.custom-shape-divider-bottom-1736569822 svg {
  position: relative;
  display: block;
  width: 150%;
  height: 90px;
}

.custom-shape-divider-bottom-1736569822 .shape-fill {
  fill: #ffffff;
}

@media (max-width: 480px) {
  .wave-banner {
    height: 150px;
  }
}

@media (max-width: 300px) {
  .wave-banner {
    height: 120px;
  }
}
</style>
