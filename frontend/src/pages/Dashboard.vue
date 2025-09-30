<!-- src/pages/Dashboard.vue -->
<template>
    <section class="max-w-5xl mx-auto px-4 py-10">
      <h1 class="text-2xl font-bold mb-6">Dashboard</h1>
  
      <div v-if="loading" class="text-gray-500">Loading…</div>
      <div v-else-if="error" class="text-red-600">{{ error }}</div>
  
      <div v-else-if="user" class="grid md:grid-cols-3 gap-6">
        <div class="md:col-span-2 bg-white rounded-xl shadow p-5">
          <h3 class="font-semibold mb-3">Profile</h3>
          <div class="space-y-1 text-sm">
            <div><b>ID:</b> {{ user.id }}</div>
            <div><b>Name:</b> {{ user.name }}</div>
            <div><b>Email:</b> {{ user.email }}</div>
            <div><b>Role:</b> {{ user.role }}</div>
          </div>
        </div>
  
        <div class="bg-white rounded-xl shadow p-5">
          <h3 class="font-semibold mb-3">Quick Actions</h3>
          <div class="flex flex-col gap-2 text-sm">
            <router-link class="px-3 py-2 bg-indigo-600 text-white rounded-md text-center"
                         to="/interview">Start an Interview</router-link>
            <router-link class="px-3 py-2 bg-gray-100 rounded-md text-center"
                         to="/mysessions">My Sessions</router-link>
            <router-link class="px-3 py-2 bg-gray-100 rounded-md text-center"
                         to="/myattempts">My Attempts</router-link>
            <button @click="logout"
                    class="px-3 py-2 bg-gray-200 rounded-md text-center">Logout</button>
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  import { useRouter } from 'vue-router'
  import { getToken, clearAuth } from '../lib/auth'
  
  const router = useRouter()
  const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  const user = ref(null)
  const loading = ref(true)
  const error = ref('')
  
  async function loadMe () {
    const token = getToken()
    if (!token) { router.push('/login'); return }
    try {
      const { data } = await axios.get(`${apiBase}/auth/me`, { headers: { Authorization: `Bearer ${token}` } })
      user.value = data
    } catch (e) {
      error.value = e?.response?.data?.detail || e.message
      clearAuth()
      router.push('/login')
    } finally {
      loading.value = false
    }
  }
  
  function logout () {
    clearAuth()
    router.push('/login')
  }
  
  onMounted(loadMe)
  </script>
  