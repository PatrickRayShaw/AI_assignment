import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { loginAPI, registerAPI, getUserInfoAPI } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const username = ref(localStorage.getItem('username') || '')
  const userInfo = ref(null)

  const isLoggedIn = computed(() => !!token.value)

  async function login(credentials) {
    const res = await loginAPI(credentials)
    token.value = res.access_token
    username.value = res.user.username
    localStorage.setItem('token', res.access_token)
    localStorage.setItem('username', res.user.username)
    await fetchUserInfo()
    return res
  }

  async function register(data) {
    return await registerAPI(data)
  }

  async function fetchUserInfo() {
    try {
      const res = await getUserInfoAPI()
      userInfo.value = res
    } catch (e) {
      console.error('Failed to fetch user info')
    }
  }

  function logout() {
    token.value = ''
    username.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('username')
  }

  return { token, username, userInfo, isLoggedIn, login, register, fetchUserInfo, logout }
})
