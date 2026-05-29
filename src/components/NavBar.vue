<template>
  <v-app-bar flat height="64" class="navbar">

    <RouterLink to="/" class="brand-link ml-4">
      <span class="brand-text">NYX</span>
    </RouterLink>

    <v-spacer />

    <div class="nav-links d-none d-md-flex mr-2">
      <v-btn variant="text" to="/" class="nav-btn">Главная</v-btn>
      <v-btn variant="text" to="/events/practice-2025-2026" class="nav-btn">Мероприятия</v-btn>
    </div>

    <div class="mr-3">
      <template v-if="!team">
        <v-btn variant="text" to="/signup" class="nav-btn mr-1">Регистрация</v-btn>
        <v-btn variant="outlined" color="secondary" to="/login" size="small" class="login-btn">Войти</v-btn>
      </template>

      <v-menu v-else offset-y>
        <template #activator="{ props }">
          <v-btn v-bind="props" variant="text" prepend-icon="mdi-account-circle" color="secondary">
            {{ team.name || team.full_name }}
          </v-btn>
        </template>
        <v-list :bg-color="isDark ? '#110e24' : '#fff'" style="border: 1px solid var(--c-card-border);">
          <v-list-item to="/dashboard" prepend-icon="mdi-view-dashboard" title="Личный кабинет" />
          <v-divider />
          <v-list-item @click="doLogout" prepend-icon="mdi-logout" title="Выйти" />
        </v-list>
      </v-menu>
    </div>

  </v-app-bar>
</template>

<script setup>
import { computed } from 'vue'
import { useTheme } from 'vuetify'
import { useRouter } from 'vue-router'
import { team, logout } from '../store/auth.js'

const router = useRouter()
const vuetifyTheme = useTheme()

// Реактивное вычисление текущей темы
const isDark = computed(() => vuetifyTheme.global.name.value === 'dark')

function toggleTheme() {
  const next = isDark.value ? 'light' : 'dark'
  vuetifyTheme.global.name.value = next
  localStorage.setItem('theme', next)   // Сохраняем выбор пользователя
}

function doLogout() {
  logout()
  router.push('/')
}
</script>

<style scoped>
.navbar {
  background: var(--c-nav-bg) !important;
  border-bottom: 1px solid var(--c-nav-border) !important;
  backdrop-filter: blur(12px);
  animation: slideDown 0.5s ease both;
}
@keyframes slideDown {
  from { opacity: 0; transform: translateY(-100%); }
  to   { opacity: 1; transform: translateY(0); }
}

.brand-link { text-decoration: none; }
.brand-text {
  font-size: 1.3rem;
  font-weight: 900;
  letter-spacing: 5px;
  color: #a78bfa;
  transition: color 0.2s;
}

.nav-links { gap: 4px; }
.nav-btn { color: rgba(128, 128, 128, 0.9); transition: color 0.2s; }
.nav-btn:hover { color: #a78bfa; }

/* Кнопка солнца/луны */
.theme-btn { color: #a78bfa !important; }
.theme-btn:hover { transform: rotate(20deg); }

/* Анимация смены иконки */
.icon-switch-enter-active, .icon-switch-leave-active { transition: opacity 0.2s, transform 0.2s; }
.icon-switch-enter-from { opacity: 0; transform: scale(0.5) rotate(-90deg); }
.icon-switch-leave-to   { opacity: 0; transform: scale(0.5) rotate(90deg); }

.login-btn {
  animation: borderPulse 2.5s ease-in-out infinite;
}
@keyframes borderPulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(167, 139, 250, 0); }
  50%       { box-shadow: 0 0 8px 2px rgba(167, 139, 250, 0.25); }
}
</style>
