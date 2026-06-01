import { ref } from 'vue'

const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

function login(userData) {
  user.value = userData
  localStorage.setItem('user', JSON.stringify(userData))
}

function logout() {
  user.value = null
  localStorage.removeItem('user')
}

export { user, login, logout }
