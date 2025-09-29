import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import Toast from "vue-toastification"
import "vue-toastification/dist/index.css"
import App from './App.vue'
import Home from './pages/Home.vue'
import Ping from './pages/Ping.vue'
import Login from './pages/Login.vue'
import Register from './pages/Register.vue'
import Scenarios from './pages/Scenarios.vue'
import StartSession from './pages/StartSession.vue'
import PlaySession from './pages/PlaySession.vue'
import SessionSummary from './pages/SessionSummary.vue'
import Admin from './pages/Admin.vue'
import { getToken } from './lib/auth'

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/ping', component: Ping, meta: { requiresAuth: true } },
  { path: '/admin', component: Admin, meta: { requiresAuth: true } },

  // Interview flow
  { path: '/interview', component: Scenarios, meta: { requiresAuth: true } },
  { path: '/interview/:scenarioId/start', component: StartSession, meta: { requiresAuth: true } },
  { path: '/interview/session/:sessionId', component: PlaySession, meta: { requiresAuth: true } },
  { path: '/interview/session/:sessionId/summary', component: SessionSummary, meta: { requiresAuth: true } },
]

const router = createRouter({ history: createWebHistory(), routes })
router.beforeEach((to) => {
  if (to.meta.requiresAuth && !getToken()) return '/login'
})

const app = createApp(App)
app.use(router)
app.use(Toast, { timeout: 3000, position: "top-right" })
app.mount('#app')
