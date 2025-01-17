<template>
    <div class="wave-header">
      <!-- Header Image -->
      <v-img
        :src="imageSrc"
        class="header-image"
        cover
      ></v-img>
  
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
          ></path>
        </svg>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  defineProps({
    imageSrc: {
      type: String,
      required: true,
      default: '@/assets/teambuilding-background.jpg'
    },
  })
  </script>
  
  <style scoped>
  .wave-header {
    position: relative;
    height: 200px; 
    overflow: hidden;
  }
  
  .header-image {
    width: 100%;
    height: 100%;
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
    width: calc(120% + 1.3px);
    height: 100px;
  }
  
  .custom-shape-divider-bottom-1736569822 .shape-fill {
    fill: #FFFFFF; 
  }
  </style>
  