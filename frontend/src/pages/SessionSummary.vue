<template>
    <section class="max-w-5xl mx-auto px-6 py-10">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">
        Session Summary #{{ sessionId }}
      </h2>
  
      <!-- Loading / Error -->
      <p v-if="loading" class="text-gray-500">Summarizing…</p>
      <p v-if="error" class="text-red-500">{{ error }}</p>
  
      <!-- Summary -->
      <div v-if="summary" class="space-y-8">
        <!-- Averages -->
        <div class="bg-white rounded-xl shadow p-6">
          <h3 class="text-lg font-semibold text-gray-700 mb-4">Averages</h3>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div
              v-for="(v, k) in summary.average_scores"
              :key="k"
              class="text-center bg-gray-50 rounded-lg p-4 shadow-sm"
            >
              <p class="text-sm text-gray-500 capitalize">{{ k }}</p>
              <p class="text-xl font-bold text-indigo-600">{{ v }}</p>
            </div>
          </div>
        </div>
  
        <!-- Summary Text -->
        <div class="bg-indigo-50 rounded-xl p-6">
          <p class="text-gray-800 whitespace-pre-line leading-relaxed">
            {{ summary.summary }}
          </p>
        </div>
        <div class="bg-white rounded-xl shadow p-6">
  <h4 class="text-lg font-semibold text-green-600 mb-3">✅ Strengths</h4>
  <ul v-if="summary.strengths && summary.strengths.length > 0" class="list-disc pl-5 space-y-2 text-gray-700">
    <li v-for="(s, i) in summary.strengths" :key="i">{{ s }}</li>
  </ul>
  <p v-else class="text-gray-400 italic">No strengths identified.</p>
</div>

<div class="bg-white rounded-xl shadow p-6">
  <h4 class="text-lg font-semibold text-red-600 mb-3">⚡ Improvements</h4>
  <ul v-if="summary.improvements && summary.improvements.length > 0" class="list-disc pl-5 space-y-2 text-gray-700">
    <li v-for="(s, i) in summary.improvements" :key="i">{{ s }}</li>
  </ul>
  <p v-else class="text-gray-400 italic">No improvements suggested.</p>
</div>

  
        <!-- Actions -->
        <div class="flex gap-4">
          <router-link
            :to="`/interview/session/${sessionId}`"
            class="px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300 transition"
          >
            Back to Session
          </router-link>
          <router-link
            to="/interview"
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
          >
            All Scenarios
          </router-link>
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
  