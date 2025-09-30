<template>
  <nav class="bg-white shadow">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center">

        <!-- Left: Brand -->
        <div class="flex items-center">
          <router-link to="/" class="text-lg font-bold text-indigo-600">
            AI Interview Coach
          </router-link>
        </div>

        <!-- Center: Links -->
        <div class="hidden md:flex space-x-6">
          <router-link to="/" class="hover:text-indigo-600">Home</router-link>
          <router-link to="/interview" class="hover:text-indigo-600">Interview</router-link>
          <router-link to="/ping" class="hover:text-indigo-600">Gemini Ping</router-link>
          <router-link 
            v-if="store.me" 
            to="/dashboard" 
            class="hover:text-indigo-600 font-medium"
          >
            Dashboard
          </router-link>
        </div>

        <!-- Right: Auth -->
        <div class="flex items-center space-x-3">
          <template v-if="!store.me">
            <router-link to="/login" class="px-4 py-2 rounded border hover:bg-gray-100">
              Login
            </router-link>
            <router-link to="/register" class="px-4 py-2 rounded bg-indigo-600 text-white hover:bg-indigo-700">
              Register
            </router-link>
          </template>

          <template v-else>
            <span class="px-3 py-1 bg-gray-100 rounded text-sm text-gray-700">
              {{ store.me.name || store.me.email }}
            </span>
            <button @click="logoutUser" class="px-3 py-1 border rounded hover:bg-gray-100">
              Logout
            </button>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { store } from "../lib/store"

function logoutUser() {
  store.logout()
  window.location.href = "/login"
}
</script>
