<template>
  <footer class="footer">
    <div class="footer-content">
      <!-- Desktop Layout -->
      <div class="desktop-layout">
        <div class="company-section">
          <img src="/oy-logo.png" alt="Ocean Youth Logo" class="company-logo" />
          <div class="link-group">
            <div class="social-icons">
              <a href="https://www.facebook.com/oceanyouth" target="_blank" class="social-link">
                <v-icon icon="mdi-facebook" color="white" size="large" />
              </a>
              <a href="https://www.instagram.com/ocean_youth/" target="_blank" class="social-link">
                <v-icon icon="mdi-instagram" color="white" size="large" />
              </a>
            </div>
            <a href="https://www.oceanyouth.org/" target="_blank" class="website-link">https://www.oceanyouth.org/</a>
          </div>
        </div>

        <p class="footerText">Copyright © 2024 Blue Crew Australia × OCEAN YOUTH</p>

        <div class="company-section">
          <img src="/bc-logo.png" alt="Blue Crew Logo" class="company-logo" />
          <div class="link-group">
            <div class="social-icons">
              <a href="https://www.facebook.com/people/Blue-Crew/61565854920450/" target="_blank" class="social-link">
                <v-icon icon="mdi-facebook" color="white" size="large" />
              </a>
              <a href="https://www.instagram.com/bluecrewaustralia" target="_blank" class="social-link">
                <v-icon icon="mdi-instagram" color="white" size="large" />
              </a>
            </div>
            <a href="https://bluecrew.com.au/" target="_blank" class="website-link">https://bluecrew.com.au/</a>
          </div>
        </div>
      </div>

      <!-- Mobile Layout -->
      <div class="mobile-layout">
        <div v-if="!isExpanded" class="mobile-footer-collapsed" @click="toggleFooter">
          <div class="learn-more">
            <v-icon icon="mdi-chevron-up" color="white" size="small" />
            <span>Learn More</span>
          </div>
          <p class="footerText mobile-text">Copyright © 2024 Blue Crew Australia × OCEAN YOUTH</p>
        </div>

        <div v-else class="mobile-footer-expanded">
          <div class="close-icon" @click="toggleFooter">
            <v-icon icon="mdi-chevron-down" color="white" />
          </div>
          <p class="footerText mobile-text">Copyright © 2024 Blue Crew Australia × OCEAN YOUTH</p>

          <div class="mobile-companies">
            <!-- Blue Crew -->
            <div class="mobile-company">
              <img src="/bc-logo.png" alt="Blue Crew Logo" class="mobile-logo" />
              <div class="mobile-links">
                <div class="mobile-social">
                  <a href="https://www.facebook.com/people/Blue-Crew/61565854920450/" target="_blank">
                    <v-icon icon="mdi-facebook" color="white" size="28" />
                  </a>
                  <a href="https://www.instagram.com/bluecrewaustralia" target="_blank">
                    <v-icon icon="mdi-instagram" color="white" size="28" />
                  </a>
                </div>
                <a href="https://bluecrew.com.au/" target="_blank" class="mobile-url">https://bluecrew.com.au/</a>
              </div>
            </div>

            <!-- Ocean Youth -->
            <div class="mobile-company">
              <img src="/oy-logo.png" alt="Ocean Youth Logo" class="mobile-logo" />
              <div class="mobile-links">
                <div class="mobile-social">
                  <a href="https://www.facebook.com/oceanyouth" target="_blank">
                    <v-icon icon="mdi-facebook" color="white" size="28" />
                  </a>
                  <a href="https://www.instagram.com/ocean_youth/" target="_blank">
                    <v-icon icon="mdi-instagram" color="white" size="28" />
                  </a>
                </div>
                <a href="https://www.oceanyouth.org/" target="_blank" class="mobile-url">https://www.oceanyouth.org/</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const isExpanded = ref(false)
const toggleFooter = () => {
  isExpanded.value = !isExpanded.value
}
</script>

<style scoped>
.footer {
  background-color: rgb(var(--v-theme-primaryBlue));
  color: white;
  width: 100%;
}

.footer-content {
  padding: 1.5rem 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* Desktop Styles */
.desktop-layout {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.company-section {
  display: flex;
  align-items: center;
  gap: 3rem;
}

.company-logo {
  height: 85px;
  width: auto;
  object-fit: contain;
}

.link-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.social-icons {
  display: flex;
  gap: 1.5rem;
}

.social-link {
  text-decoration: none;
  color: white;
}

.website-link {
  color: white;
  text-decoration: none;
  font-size: 14px;
  opacity: 0.9;
}

.footerText {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  text-align: center;
}

/* Mobile Styles */
.mobile-layout {
  display: none;
}

@media screen and (max-width: 600px) {
  .desktop-layout {
    display: none;
  }

  .mobile-layout {
    display: block;
  }

  .footer-content {
    padding: 0;
  }

  .mobile-footer-collapsed {
    padding: 1rem;
    text-align: center;
    cursor: pointer;
  }

  .learn-more {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .mobile-footer-expanded {
    padding: 1rem;
    text-align: center;
    position: relative;
  }

  .close-icon {
    position: absolute;
    top: 1.5rem;
    left: 50%;
    transform: translateX(-50%);
    cursor: pointer;
  }

  .mobile-companies {
    margin-top: 4rem;
    margin-bottom: 3rem;
    display: flex;
    flex-direction: column;
    gap: 3rem;
    align-items: flex-start;
    padding: 0 2rem;
  }

  .mobile-company {
    display: flex;
    align-items: center;
    gap: 2rem;
    width: 100%;
  }

  .mobile-logo {
    height: 75px;
    width: auto;
  }

  .mobile-links {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .mobile-social {
    display: flex;
    gap: 1.5rem;
  }

  .mobile-social a {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .mobile-url {
    color: white;
    text-decoration: none;
    font-size: 14px;
  }

  .mobile-text {
    font-size: 12px;
    margin-top: 3rem;
  }
}
</style>