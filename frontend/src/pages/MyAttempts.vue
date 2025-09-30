<template>
    <section class="max-w-5xl mx-auto px-6 py-10">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">📊 My Attempts</h2>
  
      <div v-if="loading" class="text-gray-500">Loading...</div>
      <div v-else-if="error" class="text-red-500">{{ error }}</div>
  
      <div v-else>
        <table class="w-full border-collapse bg-white rounded-xl shadow overflow-hidden">
          <thead>
            <tr class="bg-gray-100 text-left text-gray-700">
              <th class="p-3">ID</th>
              <th class="p-3">Question</th>
              <th class="p-3">Answer</th>
              <th class="p-3">Score</th>
              <th class="p-3">Created</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="a in attempts"
              :key="a.id"
              class="border-t hover:bg-gray-50"
            >
              <td class="p-3">{{ a.id }}</td>
              <td class="p-3">{{ a.question_id }}</td>
              <td class="p-3 truncate max-w-xs">{{ a.user_answer }}</td>
              <td class="p-3">
                <span
                  :class="[
                    'px-2 py-1 text-xs rounded-full font-medium',
                    a.score >= 4
                      ? 'bg-green-100 text-green-700'
                      : a.score >= 3
                      ? 'bg-yellow-100 text-yellow-700'
                      : 'bg-red-100 text-red-700'
                  ]"
                >
                  {{ a.score }}
                </span>
              </td>
              <td class="p-3">{{ new Date(a.created_at).toLocaleString() }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { api, asError } from '../lib/api'
  
  const attempts = ref([])
  const loading = ref(true)
  const error = ref('')
  
  onMounted(async () => {
    try {
      const { data } = await api.get('/interview/attempts/me')
      attempts.value = data
    } catch (e) {
      error.value = asError(e)
    } finally {
      loading.value = false
    }
  })
  </script>
  