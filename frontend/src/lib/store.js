import { reactive } from "vue"
import { getMe } from "./auth"

export const store = reactive({
  me: getMe(),

  setMe(user) {
    this.me = user
    if (user) localStorage.setItem("me", JSON.stringify(user))
    else localStorage.removeItem("me")
  },

  logout() {
    this.me = null
    localStorage.removeItem("token")
    localStorage.removeItem("me")
  }
})
