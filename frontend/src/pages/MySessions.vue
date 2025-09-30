<!-- src/pages/MySessions.vue -->
<template>
    <section class="max-w-5xl mx-auto px-4 py-10">
      <h1 class="text-2xl font-bold mb-6">My Sessions</h1>
  
      <div v-if="loading" class="text-gray-500">Loading…</div>
      <div v-else-if="error" class="text-red-600">{{ error }}</div>
  
      <div v-else>
        <div v-if="sessions.length === 0" class="text-gray-500">
          You don’t have any sessions yet.
          <router-link to="/interview" class="text-indigo-600">Start one</router-link>.
        </div>
  
        <ul v-else class="space-y-3">
          <li v-for="s in sessions" :key="s.id" class="bg-white rounded-lg shadow p-4 flex items-center justify-between">
            <div class="text-sm">
              <div><b>#{{ s.id }}</b> — scenario {{ s.scenario_id }}</div>
              <div class="text-gray-500">Status: {{ s.status }}</div>
            </div>
            <div class="flex gap-2">
              <router-link :to="`/interview/${s.id}`" class="px-3 py-1.5 bg-gray-100 rounded-md">Open</router-link>
              <router-link :to="`/interview/session/${s.id}/summary`" class="px-3 py-1.5 bg-indigo-600 text-white rounded-md">Summary</router-link>
            </div>
          </li>
        </ul>
      </div>
    </section>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  import { getToken } from '../lib/auth'
  
  const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  const sessions = ref([])
  const loading = ref(true)
  const error = ref('')
  
  onMounted(async () => {
    try {
      const token = getToken()
      const { data } = await axios.get(`${apiBase}/interview/sessions/me`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      sessions.value = data || []
    } catch (e) {
      error.value = e?.response?.data?.detail || e.message
    } finally {
      loading.value = false
    }
  })
  </script>
  