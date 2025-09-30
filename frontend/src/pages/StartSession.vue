<!-- src/pages/StartSession.vue -->
<template>
    <section class="max-w-5xl mx-auto px-4 py-10">
      <h1 class="text-2xl font-bold mb-6">Start Session</h1>
  
      <div v-if="loading" class="text-gray-500">Starting session…</div>
      <div v-else-if="error" class="text-red-600">{{ error }}</div>
  
      <div v-else-if="session">
        <p class="mb-4">Session <b>#{{ session.id }}</b> for scenario <b>{{ session.scenario_id }}</b> is <b>{{ session.status }}</b>.</p>
  
        <h3 class="font-semibold mb-2">Questions</h3>
        <ul class="list-disc ml-5 space-y-1">
          <li v-for="q in questions" :key="q.id">{{ q.text }}</li>
        </ul>
  
        <router-link :to="`/interview/session/${session.id}`"
                     class="inline-block mt-4 px-4 py-2 bg-indigo-600 text-white rounded-md">
          Begin answering
        </router-link>
      </div>
    </section>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import { api } from '../lib/api'
  import { getToken } from '../lib/auth'
  
  const route = useRoute()
  const scenarioId = Number(route.params.scenarioId)
  
  const session = ref(null)
  const questions = ref([])
  const loading = ref(true)
  const error = ref('')
  
  onMounted(async () => {
    try {
      if (!getToken()) throw new Error('Not authenticated')
      if (!scenarioId) throw new Error('Invalid scenario id')
  
      const { data: sess } = await api.post('/interview/sessions/start', { scenario_id: scenarioId })
      session.value = sess
  
      const { data: qs } = await api.get(`/scenarios/${scenarioId}/questions`)
      questions.value = qs || []
    } catch (e) {
      error.value = e?.response?.data?.detail || e.message
    } finally {
      loading.value = false
    }
  })
  </script>
  