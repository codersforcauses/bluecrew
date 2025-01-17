<template>
  <footer class="footer">
    <div class="footer-content">
      <!-- Desktop Layout -->
      <div class="desktop-layout">
        <!-- Left company section -->
        <div class="company-section">
          <img src="/oy-logo.png" alt="Ocean Youth Logo" class="company-logo" />
          <div class="social-icons">
            <a href="#" class="social-link"><v-icon icon="mdi-facebook" color="white" size="large" /></a>
            <a href="#" class="social-link"><v-icon icon="mdi-instagram" color="white" size="large" /></a>
          </div>
        </div>

        <!-- Center copyright text -->
        <p class="footerText">Copyright © 2024 Blue Crew Australia × OCEAN YOUTH</p>

        <!-- Right company section -->
        <div class="company-section">
          <img src="/bc-logo.png" alt="Blue Crew Logo" class="company-logo" />
          <div class="social-icons">
            <a href="#" class="social-link"><v-icon icon="mdi-facebook" color="white" size="large" /></a>
            <a href="#" class="social-link"><v-icon icon="mdi-instagram" color="white" size="large" /></a>
          </div>
        </div>
      </div>

      <!-- Mobile Layout -->
      <div class="mobile-layout">
        <p class="footerText">Copyright © 2024 Blue Crew Australia × OCEAN YOUTH</p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
// No setup needed
</script>

<style scoped>
.footer {
  background-color: rgb(var(--v-theme-primaryBlue));
  color: white;
  width: 100%;
}

.footer-content {
  padding: 1rem 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.desktop-layout {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.mobile-layout {
  display: none;
}

.company-section {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.company-logo {
  height: 60px;
  width: auto;
}

.social-icons {
  display: flex;
  gap: 1rem;
}

.social-link {
  text-decoration: none;
  color: white;
}

.footerText {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  text-align: center;
}

/* Mobile responsive design */
@media screen and (max-width: 600px) {
  .desktop-layout {
    display: none;
  }

  .mobile-layout {
    display: block;
  }

  .footer-content {
    padding: 1rem;
  }

  .footerText {
    font-size: 12px;
    text-align: center;
  }
}
</style>