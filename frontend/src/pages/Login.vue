<template>
    <section>
      <h2>Login</h2>
      <form @submit.prevent="submit" style="max-width:420px">
        <label>Email</label>
        <input v-model="email" type="email" required style="width:100%;margin:.25rem 0 .75rem 0" />
        <label>Password</label>
        <input v-model="password" type="password" required style="width:100%;margin:.25rem 0 1rem 0" />
        <button :disabled="loading">{{ loading ? 'Logging in...' : 'Login' }}</button>
        <p v-if="error" style="color:red;margin-top:.5rem">{{ error }}</p>
      </form>
      <p style="margin-top:1rem">No account? <router-link to="/register">Register</router-link></p>
    </section>
  </template>
  
  <script setup>
  import axios from 'axios'
  import { ref } from 'vue'
  import { setToken } from '../lib/auth'
  
  const email = ref('')
  const password = ref('')
  const loading = ref(false)
  const error = ref('')
  const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  
  const submit = async () => {
    loading.value = true; error.value = ''
    try {
      const { data } = await axios.post(`${apiBase}/auth/login`, { email: email.value, password: password.value })
      setToken(data.access_token)
      window.location.href = '/ping'
    } catch (e) {
      error.value = e?.response?.data?.detail || e.message
    } finally {
      loading.value = false
    }
  }
  </script>
  