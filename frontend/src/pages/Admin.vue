<template>
    <section style="max-width:1000px;margin:2rem auto">
      <h2>Admin Dashboard</h2>
      <p v-if="loading">Loading users…</p>
      <p v-if="error" style="color:red">{{ error }}</p>
  
      <div v-if="users.length">
        <table border="1" cellpadding="6">
          <thead>
            <tr><th>ID</th><th>Name</th><th>Email</th><th>Role</th><th>Actions</th></tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id">
              <td>{{ u.id }}</td>
              <td>{{ u.name }}</td>
              <td>{{ u.email }}</td>
              <td>{{ u.role }}</td>
              <td>
                <button @click="loadSessions(u.id)">Sessions</button>
              </td>
            </tr>
          </tbody>
        </table>
  
        <div v-if="sessions.length" style="margin-top:1rem">
          <h3>Sessions of user {{ selectedUser }}</h3>
          <ul>
            <li v-for="s in sessions" :key="s.id">
              Session #{{ s.id }} — {{ s.status }} (scenario {{ s.scenario_id }})
              <button @click="loadAttempts(s.id)">Attempts</button>
            </li>
          </ul>
        </div>
  
        <div v-if="attempts.length" style="margin-top:1rem">
          <h3>Attempts in session {{ selectedSession }}</h3>
          <ul>
            <li v-for="a in attempts" :key="a.id">
              Q{{ a.question_id }} → {{ a.user_answer }} (score {{ a.score }})
            </li>
          </ul>
        </div>
      </div>
    </section>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { api, asError } from '../lib/api'
  
  const users = ref([])
  const sessions = ref([])
  const attempts = ref([])
  const selectedUser = ref(null)
  const selectedSession = ref(null)
  const loading = ref(true)
  const error = ref('')
  
  async function loadUsers() {
    try {
      const { data } = await api.get('/admin/users')
      users.value = data
    } catch (e) {
      error.value = asError(e)
    } finally {
      loading.value = false
    }
  }
  
  async function loadSessions(uid) {
    selectedUser.value = uid
    sessions.value = []
    attempts.value = []
    try {
      const { data } = await api.get(`/admin/users/${uid}/sessions`)
      sessions.value = data
    } catch (e) {
      error.value = asError(e)
    }
  }
  
  async function loadAttempts(sid) {
    selectedSession.value = sid
    attempts.value = []
    try {
      const { data } = await api.get(`/admin/sessions/${sid}/attempts`)
      attempts.value = data
    } catch (e) {
      error.value = asError(e)
    }
  }
  
  onMounted(loadUsers)
  </script>
  