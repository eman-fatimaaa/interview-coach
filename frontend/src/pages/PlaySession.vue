<template>
  <section class="max-w-3xl mx-auto p-6">
    <h2 class="text-xl font-bold mb-4">
      Interview Session #{{ sessionId }}
    </h2>

    <!-- Show loading / error -->
    <p v-if="loading">Loading questions...</p>
    <p v-if="error" class="text-red-500">{{ error }}</p>

    <!-- Show when questions are loaded -->
    <div v-if="questions.length > 0">
      <div class="flex gap-2 mb-4">
        <button
          v-for="q in questions"
          :key="q.id"
          @click="currentQuestion = q"
          class="px-3 py-1 rounded border hover:bg-gray-100"
        >
          Q{{ q.id }}
        </button>
      </div>

      <div v-if="currentQuestion">
        <h3 class="font-semibold mb-2">
          Question #{{ currentQuestion.id }}
        </h3>
        <p class="mb-4">{{ currentQuestion.text }}</p>

        <textarea
          v-model="answer"
          placeholder="Your answer"
          class="w-full p-3 border rounded mb-4"
          rows="5"
        />

        <div class="flex gap-2">
          <button @click="submitAnswer" class="bg-indigo-600 text-white px-4 py-2 rounded">
            Submit
          </button>
          <button @click="answer = ''" class="border px-4 py-2 rounded">
            Clear
          </button>
        </div>
      </div>
    </div>

    <!-- No questions -->
    <p v-else-if="!loading && !error" class="text-gray-500">
      No questions found for this session.
    </p>

    <router-link
      v-if="!loading && questions.length > 0"
      :to="`/interview/session/${sessionId}/summary`"
      class="inline-block mt-6 text-indigo-600 hover:underline"
    >
      View Session Summary
    </router-link>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRoute } from "vue-router"
import { api, asError } from "../lib/api"

const route = useRoute()
const sessionId = Number(route.params.sessionId)

const questions = ref([])       // ✅ always initialize as empty array
const currentQuestion = ref(null)
const answer = ref("")
const loading = ref(true)
const error = ref("")

onMounted(async () => {
  try {
    const { data } = await api.get(`/interview/sessions/${sessionId}/details`)
    // adjust depending on backend response structure
    questions.value = data.questions || []
    if (questions.value.length > 0) {
      currentQuestion.value = questions.value[0]
    }
  } catch (e) {
    error.value = asError(e)
  } finally {
    loading.value = false
  }
})

async function submitAnswer() {
  if (!currentQuestion.value) return
  try {
    await api.post("/interview/answer", {
      session_id: sessionId,
      question_id: currentQuestion.value.id,
      answer: answer.value
    })
    alert("Answer submitted ✅")
  } catch (e) {
    error.value = asError(e)
  }
}
</script>
