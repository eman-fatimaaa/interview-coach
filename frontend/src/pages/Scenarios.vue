<template>
    <section style="max-width:900px;margin:2rem auto">
      <h2>Interview Scenarios</h2>
      <p v-if="loading">Loading scenarios…</p>
      <p v-if="error" style="color:red">{{ error }}</p>
      <div v-if="scenarios.length" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1rem">
        <article v-for="s in scenarios" :key="s.id" style="border:1px solid #eee;border-radius:12px;padding:1rem">
          <h3 style="margin:.25rem 0">{{ s.title }}</h3>
          <div style="font-size:.9rem;color:#666">{{ s.role }} • {{ s.level }}</div>
          <p style="margin:.5rem 0 1rem 0">{{ s.description }}</p>
          <router-link :to="`/interview/${s.id}/start`">
            <button>Start</button>
          </router-link>
        </article>
      </div>
    </section>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { api, asError } from '../lib/api'
  
  const scenarios = ref([])
  const loading = ref(true)
  const error = ref('')
  
  onMounted(async () => {
    try {
      const { data } = await api.get('/scenarios')
      scenarios.value = data
    } catch (e) {
      error.value = asError(e)
    } finally {
      loading.value = false
    }
  })
  </script>
  