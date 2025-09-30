<!-- src/pages/Scenarios.vue -->
<template>
    <section class="max-w-6xl mx-auto px-4 py-10">
      <h1 class="text-2xl font-bold mb-6">Choose a Scenario</h1>
  
      <div v-if="loading" class="text-gray-500">Loading…</div>
      <div v-else-if="error" class="text-red-600">{{ error }}</div>
  
      <div v-else class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="s in scenarios" :key="s.id" class="bg-white rounded-xl shadow p-5 flex flex-col">
          <h3 class="font-semibold">{{ s.title }}</h3>
          <p class="text-sm text-gray-500 mt-1">{{ s.role }} • {{ s.level }}</p>
          <p class="text-sm text-gray-600 mt-3 line-clamp-3">{{ s.description }}</p>
          <router-link :to="`/interview/${s.id}/start`"
                       class="mt-4 px-3 py-2 bg-indigo-600 text-white rounded-md text-center">
            Start
          </router-link>
        </div>
      </div>
    </section>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { api } from '../lib/api'
  import { getToken } from '../lib/auth'
  
  const scenarios = ref([])
  const loading = ref(true)
  const error = ref('')
  
  onMounted(async () => {
    try {
      // api instance already attaches token, but keep a hard auth check here:
      if (!getToken()) throw new Error('Not authenticated')
      const { data } = await api.get('/scenarios')
      scenarios.value = data || []
    } catch (e) {
      error.value = e?.response?.data?.detail || e.message
    } finally {
      loading.value = false
    }
  })
  </script>
  