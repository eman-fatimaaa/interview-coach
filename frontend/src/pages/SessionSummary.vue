<template>
    <section style="max-width:900px;margin:2rem auto">
      <h2>Session Summary #{{ sessionId }}</h2>
  
      <p v-if="loading">Summarizing…</p>
      <p v-if="error" style="color:red">{{ error }}</p>
  
      <div v-if="summary">
        <div style="margin:.75rem 0">
          <b>Averages:</b>
          <ul>
            <li v-for="(v,k) in summary.average_scores" :key="k">
              {{ k }}: {{ v }}
            </li>
          </ul>
        </div>
  
        <article style="border:1px solid #eee;border-radius:12px;padding:1rem;background:#fafafa">
          <p style="white-space:pre-wrap">{{ summary.summary }}</p>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1rem">
            <div>
              <h4>Strengths</h4>
              <ul><li v-for="(s,i) in summary.strengths" :key="i">{{ s }}</li></ul>
            </div>
            <div>
              <h4>Improvements</h4>
              <ul><li v-for="(s,i) in summary.improvements" :key="i">{{ s }}</li></ul>
            </div>
          </div>
        </article>
  
        <div style="margin-top:1rem;display:flex;gap:.5rem">
          <router-link :to="`/interview/session/${sessionId}`"><button>Back to session</button></router-link>
          <router-link to="/interview"><button>All scenarios</button></router-link>
        </div>
      </div>
    </section>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import { api, asError } from '../lib/api'
  
  const route = useRoute()
  const sessionId = Number(route.params.sessionId)
  
  const summary = ref(null)
  const loading = ref(true)
  const error = ref('')
  
  onMounted(async () => {
    try {
      const { data } = await api.get(`/interview/sessions/${sessionId}/summary`)
      summary.value = data
    } catch (e) {
      error.value = asError(e)
    } finally {
      loading.value = false
    }
  })
  </script>
  