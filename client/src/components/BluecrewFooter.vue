<template>
    <footer class="footer">
        <p class="footerText">Copyright © 2024 Blue Crew Australia</p>
    </footer>
</template>

<script lang="ts">
export default {
  name: "BluecrewFooter",
};
</script>

<style scoped>

  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
  .footer{
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
    font-family: 'Poppins', sans-serif;
  } 

  .footerText {
    margin: 0;
    line-height: 100px;
    font-weight: 300;
  }

  @media screen and (max-width: 768px) {
    .footer{
      height: 50px;
      font-size: 12px;
    }
    .footerText{
      font-weight: 100;
      line-height: 50px;
    }
  }
</style>