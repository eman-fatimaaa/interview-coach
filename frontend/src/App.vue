
<template>
  <div>
    <NavBar />
    <main style="max-width: 900px; margin: 2rem auto; padding: 1rem;">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import NavBar from './components/NavBar.vue'
</script>
