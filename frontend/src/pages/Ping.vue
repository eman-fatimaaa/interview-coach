
<template>
  <section>
    <h2>Gemini Ping</h2>
    <p>Send a prompt to the backend, which calls Gemini and returns a reply.</p>
    <form @submit.prevent="sendPrompt" style="margin-top:1rem">
      <textarea v-model="prompt" rows="4" style="width:100%" placeholder="Type a prompt..."></textarea>
      <button :disabled="loading" style="margin-top:0.5rem; padding:0.5rem 1rem;">{{ loading ? 'Sending...' : 'Send' }}</button>
    </form>
    <div v-if="error" style="margin-top:1rem; color:red">
      <strong>Error:</strong> {{ error }}
    </div>
    <div v-if="reply" style="margin-top:1rem; white-space:pre-wrap;">
      <strong>Reply:</strong>
      <p>{{ reply }}</p>
    </div>
  </section>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { authHeader } from '../lib/auth'

const prompt = ref('Say hello in a friendly way.')
const reply = ref('')
const error = ref('')
const loading = ref(false)
const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const sendPrompt = async () => {
  loading.value = true
  error.value = ''
  reply.value = ''
  try {
    const { data } = await axios.post(`${apiBase}/ai/ping`, { prompt: prompt.value }, { headers: { ...authHeader() } })
    reply.value = data.reply
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message
  } finally {
    loading.value = false
  }
}
</script>

