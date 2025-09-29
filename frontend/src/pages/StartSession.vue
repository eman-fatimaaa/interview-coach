<template>
    <section style="max-width:900px;margin:2rem auto">
      <h2>Start Session</h2>
      <p v-if="loading">Starting session…</p>
      <p v-if="error" style="color:red">{{ error }}</p>
  
      <div v-if="session">
        <p>Session <b>#{{ session.id }}</b> for scenario <b>{{ session.scenario_id }}</b> is <b>{{ session.status }}</b>.</p>
        <h3>Questions</h3>
        <ul>
          <li v-for="q in questions" :key="q.id" style="margin:.5rem 0">
            <span>#{{ q.id }} — {{ q.text }}</span>
          </li>
        </ul>
        <router-link :to="`/interview/session/${session.id}`">
          <button>Begin answering</button>
        </router-link>
      </div>
    </section>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import { api, asError } from '../lib/api'
  
  const route = useRoute()
  const scenarioId = Number(route.params.scenarioId)
  
  const session = ref(null)
  const questions = ref([])
  const loading = ref(true)
  const error = ref('')
  
  onMounted(async () => {
    try {
      // start a new session
      const { data: sess } = await api.post('/interview/sessions/start', { scenario_id: scenarioId })
      session.value = sess
      // load questions for display
      const { data: qs } = await api.get(`/scenarios/${scenarioId}/questions`)
      questions.value = qs
    } catch (e) {
      error.value = asError(e)
    } finally {
      loading.value = false
    }
  })
  </script>
  