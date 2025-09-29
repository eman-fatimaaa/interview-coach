<template>
    <section style="max-width:900px;margin:2rem auto">
      <h2>Interview Session #{{ sessionId }}</h2>
  
      <div v-if="loading">Loading…</div>
      <p v-if="error" style="color:red">{{ error }}</p>
  
      <div v-if="questions.length">
        <div style="display:flex;gap:.5rem;flex-wrap:wrap;margin:.5rem 0 1rem 0">
          <button
            v-for="q in questions" :key="q.id"
            :class="['tab', {active: q.id === currentQuestionId}]"
            @click="selectQuestion(q.id)"
          >
            Q{{ q.id }}
          </button>
        </div>
  
        <article v-if="currentQuestion" style="border:1px solid #eee;border-radius:12px;padding:1rem">
          <h3>Question #{{ currentQuestion.id }}</h3>
          <p style="margin:.5rem 0 1rem 0">{{ currentQuestion.text }}</p>
  
          <label>Your answer</label>
          <textarea v-model="answer" rows="6" style="width:100%;margin:.25rem 0 1rem 0"></textarea>
  
          <div style="display:flex;gap:.5rem;align-items:center">
            <button :disabled="busy || answer.trim().length<2" @click="submitAnswer">
              {{ busy ? 'Submitting…' : 'Submit' }}
            </button>
            <button @click="clear" :disabled="busy">Clear</button>
          </div>
  
          <div v-if="lastAttempt" style="margin-top:1rem;padding:.75rem;border-radius:10px;background:#fafafa;border:1px solid #eee">
            <h4 style="margin:.25rem 0 .5rem 0">AI Feedback</h4>
            <div v-if="lastAttempt.parsed">
              <p style="white-space:pre-wrap">{{ lastAttempt.parsed.feedback }}</p>
              <p style="margin-top:.5rem"><b>Overall:</b> {{ lastAttempt.parsed.overall_score }}</p>
              <p>
                <b>Rubric:</b>
                Relevance {{ lastAttempt.parsed.rubric?.relevance ?? '—' }} •
                STAR {{ lastAttempt.parsed.rubric?.star_structure ?? '—' }} •
                Tech {{ lastAttempt.parsed.rubric?.technical_depth ?? '—' }} •
                Comm {{ lastAttempt.parsed.rubric?.communication ?? '—' }}
              </p>
            </div>
            <div v-else>
              <p style="white-space:pre-wrap">{{ lastAttempt.ai_feedback }}</p>
              <p><b>Overall:</b> {{ lastAttempt.score ?? '—' }}</p>
            </div>
          </div>
        </article>
  
        <div style="margin-top:1.25rem;display:flex;gap:.5rem">
          <router-link :to="`/interview/session/${sessionId}/summary`">
            <button>View Session Summary</button>
          </router-link>
        </div>
      </div>
    </section>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue'
  import { useRoute } from 'vue-router'
  import { api, asError } from '../lib/api'
  import { watch } from 'vue'
  import { useToast } from "vue-toastification"

  
  const route = useRoute()
  const sessionId = Number(route.params.sessionId)
  
  const questions = ref([])
  const currentQuestionId = ref(null)
  const answer = ref('')
  const busy = ref(false)
  const loading = ref(true)
  const error = ref('')
  const lastAttempt = ref(null)
  const toast = useToast()
  
  const currentQuestion = computed(() => questions.value.find(q => q.id === currentQuestionId.value))
  
  function selectQuestion(id) {
    currentQuestionId.value = id
    answer.value = ''
    lastAttempt.value = null
  }
  
  function parseAttempt(attempt) {
    try {
      const parsed = JSON.parse(attempt.ai_feedback)
      return { ...attempt, parsed }
    } catch {
      return attempt
    }
  }
  
  function clear() {
    answer.value = ''
  }
  
  async function submitAnswer() {
  busy.value = true; error.value = ''
  try {
    const { data } = await api.post('/interview/answer', {
      session_id: sessionId,
      question_id: currentQuestionId.value,
      answer: answer.value
    })
    lastAttempt.value = parseAttempt(data)
    toast.success("Answer evaluated ✅")
  } catch (e) {
    error.value = asError(e)
    toast.error(error.value)
  } finally {
    busy.value = false
  }
}
  
  onMounted(async () => {
    try {
      // load session to know scenario id
      const { data: sessions } = await api.get('/interview/sessions/me')
      const sess = sessions.find(s => s.id === sessionId)
      if (!sess) { error.value = 'Session not found'; return }
  
      const { data: qs } = await api.get(`/scenarios/${sess.scenario_id}/questions`)
      questions.value = qs
      if (qs.length) currentQuestionId.value = qs[0].id
    } catch (e) {
      error.value = asError(e)
    } finally {
      loading.value = false
    }
  })
  watch(currentQuestionId, (id) => {
  if (id) localStorage.setItem(`session-${sessionId}-currentQ`, String(id))
})

onMounted(async () => {
  try {
    // ...load qs...
    const saved = localStorage.getItem(`session-${sessionId}-currentQ`)
    if (saved && qs.find(q => q.id === Number(saved))) {
      currentQuestionId.value = Number(saved)
    } else if (qs.length) {
      currentQuestionId.value = qs[0].id
    }
  } catch (e) {
    error.value = asError(e)
  } finally {
    loading.value = false
  }
})
  </script>
  
  <style scoped>
  .tab { padding:.35rem .6rem; border:1px solid #ddd; background:#fff; border-radius:8px; cursor:pointer }
  .tab.active { background:#f3f6ff; border-color:#b7c3ff }
  </style>
  