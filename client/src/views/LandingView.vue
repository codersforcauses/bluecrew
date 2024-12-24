<script setup lang="ts">
//import { useDisplay } from 'vuetify' // Used to figure out if page is landscape/portrait
</script>

<template>
    <div class="landing-page">
      <!-- Top Image Section -->
      <div class="image-section">
        <img src="/beach-header.jpg" alt="Ocean Beach" class="image" />
      </div>
  
      <!-- Content Section -->
      <div class="content-section">
        <div class="content">
          <div class="logo">
            <img src="/bc-logo.png" alt="Blue Crew Logo" />
          </div>
          <h2 class="tagline">
            The inspiring way to become an ocean champion and protect our blue planet
          </h2>
          <div class="buttons">
            <button class="btn btn-primary">Get Started</button>
            <button class="btn btn-secondary">Have an Account?</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  

  <style scoped>
  /* Root container */
  .landing-page {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }
  
  /* Top Image Section */
  .image-section {
    flex: 1;
    background: url('/beach-header.jpg') no-repeat center center;
    background-size: cover;
  }

  .image-section img{
    width: 100%;
    height: 20%;
  }
  
  /* Content Section */
  .content-section {
    display: flex;
    flex: 1;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    padding: 2rem;
    background-color: white;
  }
  
  /* Content alignment */
  .content {
    text-align: center;
    max-width: 400px;
  }
  
  .logo img {
    width: 100px;
    margin-bottom: 1rem;
  }
  
  .tagline {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 2rem;
  }
  
  .buttons {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  /* Button styling */
  .btn {
    padding: 1rem 2rem;
    font-size: 1rem;
    border-radius: 8px;
    border: none;
    cursor: pointer;
  }
  
  .btn-primary {
    background-color: #c2185b;
    color: white;
  }
  
  .btn-secondary {
    background-color: #003c8f;
    color: white;
  }
  
  /* Responsive Design */
  @media (max-width: 768px) {
    .content-section {
      flex-direction: column;
    }
  
    .buttons {
      flex-direction: column;
    }
  }
  </style>
  