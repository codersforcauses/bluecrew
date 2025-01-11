<script setup lang="ts">
defineProps<{
  avatarIndex: number
  name: string
}>()
</script>

<template>
    <v-col class="rounded-lg d-flex ga-3 px-5 outline align-center bg-creamWhite text-primaryGrey">
      <v-img
        class="rounded-circle"
        max-height="32"
        max-width="32"
        min-width="32"
        cover
        src="https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg"
      ></v-img>
      <v-text class="me-auto font-weight-bold truncate-name">{{ name }}</v-text>
      <slot name="default"></slot>
      <slot name="acceptreject"></slot>
      <slot name="dismiss"></slot>
      <slot name="delete"></slot>
      <slot name="addfriend"></slot>
      <slot name="accept"></slot>
    </v-col>
  </template>
  
  <style scoped>
  .truncate-name {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .acceptreject {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-right: 8px;
  }
  
  .dismiss-action {
    margin-left: 8px;
  }
  
  .dismiss-btn {
    background-color: #1B2B4B !important; /* Dark blue color from the image */
    color: white !important;
    text-transform: none;
    border-radius: 8px;
  }
  </style>