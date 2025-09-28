<template>
    <section>
      <h2>Register</h2>
      <form @submit.prevent="submit" style="max-width:420px">
        <label>Name</label>
        <input v-model="name" required style="width:100%;margin:.25rem 0 .75rem 0" />
        <label>Email</label>
        <input v-model="email" type="email" required style="width:100%;margin:.25rem 0 .75rem 0" />
        <label>Password</label>
        <input v-model="password" type="password" required style="width:100%;margin:.25rem 0 1rem 0" />
        <button :disabled="loading">{{ loading ? 'Creating...' : 'Create account' }}</button>
        <p v-if="error" style="color:red;margin-top:.5rem">{{ error }}</p>
        <p v-if="ok" style="color:green;margin-top:.5rem">Account created. You can now <router-link to="/login">login</router-link>.</p>
      </form>
    </section>
  </template>
  
  <script setup>
  import axios from 'axios'
  import { ref } from 'vue'
  
  const name = ref('')
  const email = ref('')
  const password = ref('')
  const loading = ref(false)
  const error = ref('')
  const ok = ref(false)
  const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  
  const submit = async () => {
    loading.value = true; error.value = ''; ok.value = false
    try {
      await axios.post(`${apiBase}/auth/register`, { name: name.value, email: email.value, password: password.value })
      ok.value = true
    } catch (e) {
      error.value = e?.response?.data?.detail || e.message
    } finally {
      loading.value = false
    }
  }
  </script>
  