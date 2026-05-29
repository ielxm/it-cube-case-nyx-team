import { ref } from 'vue'

// Загружаем данные команды из localStorage (чтобы не терялись при обновлении страницы)
const team = ref(JSON.parse(localStorage.getItem('team') || 'null'))

function login(teamData) {
  team.value = teamData
  localStorage.setItem('team', JSON.stringify(teamData))
}

function logout() {
  team.value = null
  localStorage.removeItem('team')
  localStorage.removeItem('teamData')
}

export { team, login, logout }
