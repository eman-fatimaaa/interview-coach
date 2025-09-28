
<template>
  <header style="border-bottom:1px solid #eaeaea;padding:1rem;">
    <nav style="display:flex;align-items:center;gap:1rem;">
      <h1 style="margin:0;">AI Interview Coach</h1>
      <router-link to="/">Home</router-link>
      <router-link to="/ping">Gemini Ping</router-link>
      <span style="flex:1"></span>
      <template v-if="token">
        <button @click="onLogout">Logout</button>
      </template>
      <template v-else>
        <router-link to="/login">Login</router-link>
        <router-link to="/register">Register</router-link>
      </template>
    </nav>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getToken, logout } from '../lib/auth'
const token = ref(null)
onMounted(() => token.value = getToken())
const onLogout = () => { logout(); window.location.href = '/' }
</script>
