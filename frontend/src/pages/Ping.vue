<template>
  <section class="max-w-2xl mx-auto py-16 px-6">
    <div class="bg-white shadow-lg rounded-lg p-8 border border-gray-100">
      <h2 class="text-2xl font-bold text-gray-800 mb-2 flex items-center gap-2">
        🤖 Gemini Ping
      </h2>
      <p class="text-gray-500 mb-6">
        Send a prompt to the backend, which calls Gemini and returns a reply.
      </p>

      <!-- Input box -->
      <textarea
        v-model="prompt"
        placeholder="Type your message..."
        rows="4"
        class="w-full border border-gray-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-indigo-500"
      ></textarea>

      <!-- Buttons -->
      <div class="flex justify-end gap-3 mt-4">
        <button
          @click="sendPing"
          :disabled="loading"
          class="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition disabled:opacity-50"
        >
          {{ loading ? "Sending..." : "Send" }}
        </button>
        <button
          @click="prompt = ''; reply = ''"
          class="border px-6 py-2 rounded-lg hover:bg-gray-100"
        >
          Clear
        </button>
      </div>

      <!-- Reply -->
      <div v-if="reply" class="mt-6 bg-gray-50 border rounded-lg p-4">
        <h3 class="font-semibold text-gray-700 mb-2">Gemini’s Reply:</h3>
        <p class="text-gray-800 whitespace-pre-wrap">{{ reply }}</p>
      </div>

      <!-- Error -->
      <p v-if="error" class="mt-4 text-red-500 font-medium">
        {{ error }}
      </p>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue"
import { api, asError } from "../lib/api"

const prompt = ref("Say hello in a friendly way.")
const reply = ref("")
const error = ref("")
const loading = ref(false)

async function sendPing() {
  loading.value = true
  error.value = ""
  reply.value = ""

  try {
    const { data } = await api.post("/ai/ping", { prompt: prompt.value })
    reply.value = data.reply || "No response"
  } catch (e) {
    error.value = asError(e)
  } finally {
    loading.value = false
  }
}
</script>
