<template>
    <section class="flex justify-center items-center min-h-screen bg-gray-50">
      <div class="bg-white shadow-lg rounded-xl p-8 w-full max-w-md">
        <h2 class="text-2xl font-bold text-center mb-6 text-gray-800">
          Welcome Back 👋
        </h2>
  
        <form @submit.prevent="submit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Email</label>
            <input
              v-model="email"
              type="email"
              required
              class="mt-1 block w-full border border-gray-300 rounded-lg p-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
  
          <div>
            <label class="block text-sm font-medium text-gray-700">Password</label>
            <input
              v-model="password"
              type="password"
              required
              class="mt-1 block w-full border border-gray-300 rounded-lg p-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
  
          <button
            type="submit"
            :disabled="loading"
            class="w-full py-2 rounded-lg bg-indigo-600 text-white font-medium hover:bg-indigo-700 disabled:opacity-50"
          >
            {{ loading ? "Logging in..." : "Login" }}
          </button>
  
          <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>
        </form>
  
        <p class="mt-4 text-center text-sm">
          No account?
          <router-link to="/register" class="text-indigo-600 hover:underline">Register</router-link>
        </p>
      </div>
    </section>
  </template>
  
  <script setup>
  import { ref } from "vue"
  import { api, asError } from "../lib/api"
  import { setToken } from "../lib/auth"
  import { store } from "../lib/store"
  
  const email = ref("")
  const password = ref("")
  const loading = ref(false)
  const error = ref("")
  
  async function submit() {
    loading.value = true
    error.value = ""
    try {
      // 🔹 Login request
      const { data: login } = await api.post("/auth/login", {
        email: email.value,
        password: password.value,
      })
  
      // 🔹 Save token
      setToken(login.access_token)
  
      // 🔹 Fetch user profile
      const { data: me } = await api.get("/auth/me")
  
      // 🔹 Update store (reactive for NavBar)
      store.setMe(me)
  
      // Redirect to dashboard
      window.location.href = "/dashboard"
    } catch (e) {
      error.value = asError(e)
    } finally {
      loading.value = false
    }
  }
  </script>
  