<template>
  <footer class="footer">
    <div :class="smAndDown ? 'footer-content-mobile' : 'footer-content'">
      <!-- Desktop Layout -->
      <div v-if="!smAndDown" class="desktop-layout">
        <div class="company-section">
          <img src="/OY-logo-white.svg" alt="Ocean Youth Logo" class="company-logo" />
          <div class="link-group">
            <div class="social-icons">
              <a href="https://www.facebook.com/oceanyouth" target="_blank" class="social-link">
                <v-icon icon="mdi-facebook" color="white" size="large" />
              </a>
              <a href="https://www.instagram.com/ocean_youth/" target="_blank" class="social-link">
                <v-icon icon="mdi-instagram" color="white" size="large" />
              </a>
            </div>
            <a href="https://www.oceanyouth.org/" target="_blank" class="website-link">
              https://www.oceanyouth.org/
            </a>
          </div>
        </div>

        <p class="footerText">Copyright © 2025 Blue Crew Australia x OCEAN YOUTH</p>

        <div class="company-section">
          <img src="/bc-logo.png" alt="Blue Crew Logo" class="company-logo" />
          <div class="link-group">
            <div class="social-icons">
              <a
                href="https://www.facebook.com/people/Blue-Crew/61565854920450/"
                target="_blank"
                class="social-link"
              >
                <v-icon icon="mdi-facebook" color="white" size="large" />
              </a>
              <a
                href="https://www.instagram.com/bluecrewaustralia"
                target="_blank"
                class="social-link"
              >
                <v-icon icon="mdi-instagram" color="white" size="large" />
              </a>
            </div>
            <a href="https://bluecrew.com.au/" target="_blank" class="website-link">
              https://bluecrew.com.au/
            </a>
          </div>
        </div>
      </div>

      <!-- Mobile Layout -->
      <div v-else class="mobile-layout">
        <div v-if="!isExpanded" class="mobile-footer-collapsed" @click="toggleFooter">
          <div class="learn-more">
            <v-icon icon="mdi-chevron-up" color="white" size="small" />
            <span>Learn More</span>
          </div>
          <p class="footerText mobile-text">Copyright © 2025 Blue Crew Australia x OCEAN YOUTH</p>
        </div>

        <div v-else class="mobile-footer-expanded">
          <div class="close-icon" @click="toggleFooter">
            <v-icon icon="mdi-chevron-down" color="white" />
          </div>
          <p class="footerText mobile-text">Copyright © 2025 Blue Crew Australia x OCEAN YOUTH</p>

          <div class="mobile-companies">
            <!-- Blue Crew -->
            <div class="mobile-company">
              <div class="company-content">
                <img src="/bc-logo.png" alt="Blue Crew Logo" class="mobile-logo" />
                <div class="mobile-links">
                  <div class="mobile-social">
                    <a
                      href="https://www.facebook.com/people/Blue-Crew/61565854920450/"
                      target="_blank"
                    >
                      <v-icon icon="mdi-facebook" color="white" size="28" />
                    </a>
                    <a href="https://www.instagram.com/bluecrewaustralia" target="_blank">
                      <v-icon icon="mdi-instagram" color="white" size="28" />
                    </a>
                  </div>
                  <a href="https://bluecrew.com.au/" target="_blank" class="mobile-url">
                    https://bluecrew.com.au/
                  </a>
                </div>
              </div>
            </div>

            <!-- Ocean Youth -->
            <div class="mobile-company">
              <div class="company-content">
                <img src="/OY-logo-white.svg" alt="Ocean Youth Logo" class="mobile-logo" />
                <div class="mobile-links">
                  <div class="mobile-social">
                    <a href="https://www.facebook.com/oceanyouth" target="_blank">
                      <v-icon icon="mdi-facebook" color="white" size="28" />
                    </a>
                    <a href="https://www.instagram.com/ocean_youth/" target="_blank">
                      <v-icon icon="mdi-instagram" color="white" size="28" />
                    </a>
                  </div>
                  <a href="https://www.oceanyouth.org/" target="_blank" class="mobile-url">
                    https://www.oceanyouth.org/
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { useDisplay } from 'vuetify'
import { ref } from 'vue'

const { smAndDown } = useDisplay()
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
  bottom: 0;
  left: 0;
}

.footer-content {
  padding: 1.5rem 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.footer-content-mobile {
  padding: 0.1rem 1rem;
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

/* Mobile Layout */
.mobile-layout {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.mobile-footer-collapsed {
  padding: 0.5rem;
  text-align: center;
  cursor: pointer;
}

.mobile-footer-expanded {
  padding: 0.5rem;
  text-align: center;
}

.close-icon {
  cursor: pointer;
}

.mobile-companies {
  margin: 3rem auto;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  align-items: center;
}

.company-content {
  display: flex;
  align-items: center;
  gap: 2rem;
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
  gap: 1rem;
}

.mobile-url {
  color: white;
  text-decoration: none;
  font-size: 14px;
}

.mobile-text {
  font-size: 12px;
  margin-top: 2rem;
}
</style>
