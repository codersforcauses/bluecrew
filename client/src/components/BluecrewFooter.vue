<template>
  <footer class="footer">
    <p class="footerText">Copyright © 2024 Blue Crew Australia</p>
  </footer>
</template>

<script setup lang="ts"></script>

<style scoped>
.footer {
  background-color: #193855;
  width: 100%;
  height: 100px;
  text-align: center;
  position: fixed;
  display: flex;
  align-items: center;
  justify-content: center;
  bottom: 0;
  left: 0;
  z-index: 1000;
  color: white;
  font-size: 20px;
}

.footerText {
  margin: 0;
  line-height: 100px;
  font-weight: 300;
}

/*setup the mobile and desktop version division*/
@media screen and (max-width: 600px) {
  .footer {
    height: 50px;
    font-size: 12px;
  }
  .footerText {
    font-weight: 100;
    line-height: 50px;
  }
}
</style>
