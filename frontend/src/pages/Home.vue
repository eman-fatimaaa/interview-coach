<template>
  <div class="min-h-screen flex flex-col">
    <!-- Hero Section -->
    <section class="flex flex-1 items-center justify-center text-center px-6 py-20 bg-gray-50">
      <div class="w-full">
        <h1 class="text-5xl md:text-6xl font-extrabold mb-6 text-gray-800">
          Welcome to <span class="text-indigo-600">AI Interview Coach</span> 🎤
        </h1>
        <p class="text-lg md:text-xl mb-10 text-gray-600">
          Practice real interview scenarios with instant AI feedback. 
          Get personalized insights and boost your confidence before the big day.
        </p>
        <div class="flex justify-center gap-6">
          <router-link
            to="/register"
            class="px-8 py-4 bg-indigo-600 text-white rounded-lg shadow hover:bg-indigo-500 transition font-semibold text-lg"
          >
            Get Started
          </router-link>
          <router-link
            to="/login"
            class="px-8 py-4 bg-gray-200 text-gray-800 rounded-lg shadow hover:bg-gray-300 transition font-semibold text-lg"
          >
            Login
          </router-link>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-20 bg-gray-100">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-10 px-12">
        <div class="p-10 bg-white rounded-xl shadow hover:shadow-lg transition text-center">
          <h3 class="text-2xl font-bold text-indigo-600 mb-3">🚀 AI Feedback</h3>
          <p class="text-gray-600">Get real-time evaluation of your answers with actionable insights.</p>
        </div>
        <div class="p-10 bg-white rounded-xl shadow hover:shadow-lg transition text-center">
          <h3 class="text-2xl font-bold text-indigo-600 mb-3">🎯 Real Scenarios</h3>
          <p class="text-gray-600">Practice role-based scenarios (Backend, Frontend, System Design, etc.).</p>
        </div>
        <div class="p-10 bg-white rounded-xl shadow hover:shadow-lg transition text-center">
          <h3 class="text-2xl font-bold text-indigo-600 mb-3">📊 Progress Tracking</h3>
          <p class="text-gray-600">Track your performance over time and see your improvement clearly.</p>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="py-8 text-center text-gray-500 text-sm bg-white border-t">
      © 2025 AI Interview Coach — All Rights Reserved
    </footer>
  </div>
</template>



<script setup>
</script>
