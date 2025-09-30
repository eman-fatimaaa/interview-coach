<template>
    <div class="flex min-h-screen bg-gray-50 items-center justify-center">
      <div class="w-full max-w-md bg-white p-8 rounded-xl shadow-lg">
        <h2 class="text-2xl font-bold text-center text-gray-800">Create Account ✨</h2>
        <p class="text-sm text-center text-gray-500 mb-6">Register to start practicing interviews</p>
  
        <form @submit.prevent="submit" class="space-y-4">
          <!-- Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700">Name</label>
            <input
              v-model="name"
              type="text"
              required
              placeholder="Your Name"
              class="mt-1 w-full rounded-lg border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 shadow-sm px-3 py-2"
            />
          </div>
  
          <!-- Email -->
          <div>
            <label class="block text-sm font-medium text-gray-700">Email</label>
            <input
              v-model="email"
              type="email"
              required
              placeholder="you@example.com"
              class="mt-1 w-full rounded-lg border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 shadow-sm px-3 py-2"
            />
          </div>
  
          <!-- Password -->
          <div>
            <label class="block text-sm font-medium text-gray-700">Password</label>
            <input
              v-model="password"
              type="password"
              required
              placeholder="••••••••"
              class="mt-1 w-full rounded-lg border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 shadow-sm px-3 py-2"
            />
          </div>
  
          <!-- Role -->
          <div>
            <label class="block text-sm font-medium text-gray-700">Role</label>
            <select
              v-model="role"
              required
              class="mt-1 w-full rounded-lg border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 shadow-sm px-3 py-2"
            >
              <option value="user">User</option>
              <option value="admin">Admin</option>
            </select>
          </div>
  
          <!-- Submit -->
          <button
            :disabled="loading"
            type="submit"
            class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 rounded-lg shadow-md transition"
          >
            {{ loading ? "Creating account..." : "Register" }}
          </button>
  
          <!-- Error -->
          <p v-if="error" class="text-center text-sm text-red-500 font-medium mt-2">
            {{ error }}
          </p>
  
          <!-- Success -->
          <p v-if="success" class="text-center text-sm text-green-600 font-medium mt-2">
            🎉 Account created successfully! You can now login.
          </p>
        </form>
  
        <!-- Footer -->
        <p class="mt-6 text-sm text-center text-gray-600">
          Already have an account?
          <router-link to="/login" class="text-indigo-600 font-semibold hover:underline">
            Login here
          </router-link>
        </p>
      </div>
    </div>
  </template>
  
  
  <script setup>
  import { ref } from 'vue'
import { api, asError } from '../lib/api'
  import axios from 'axios'

  
  const name = ref('')
  const email = ref('')
  const password = ref('')
  const loading = ref(false)
  const error = ref('')
  const success = ref(false)
  const role = ref('user')
  const ok = ref(false)
  const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  
//   const submit = async () => {
//     loading.value = true; error.value = ''; ok.value = false
//     try {
//       await axios.post(`${apiBase}/auth/register`, { name: name.value, email: email.value, password: password.value })
//       ok.value = true
//     } catch (e) {
//       error.value = e?.response?.data?.detail || e.message
//     } finally {
//       loading.value = false
//     }
//   }
  async function submit() {
  loading.value = true
  error.value = ''
  success.value = false
  try {
    await api.post('/auth/register', {
      name: name.value,
      email: email.value,
      password: password.value,
      role: role.value
    })
    success.value = true
    name.value = ''
    email.value = ''
    password.value = ''
    role.value = 'user'
  } catch (e) {
    error.value = asError(e)
  } finally {
    loading.value = false
  }
}
  </script>
  