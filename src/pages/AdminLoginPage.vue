<template>
  <v-container class="py-8" style="max-width: 400px;">
    <div class="text-center mb-8 anim-fade-up">
      <v-icon size="64" color="secondary" class="mb-4">mdi-shield-admin</v-icon>
      <h1 class="text-h4 font-weight-bold mb-2">Админ-панель</h1>
      <p class="text-secondary">Введите ваши учетные данные администратора</p>
    </div>

    <v-card class="dash-card pa-6 anim-fade-up delay-1">
      <v-form @submit.prevent="handleLogin">
        <v-text-field
          v-model="email"
          label="Email администратора"
          type="email"
          variant="outlined"
          prepend-inner-icon="mdi-email"
          class="mb-4"
          required
        />

        <v-text-field
          v-model="password"
          label="Пароль"
          type="password"
          variant="outlined"
          prepend-inner-icon="mdi-lock"
          class="mb-4"
          required
        />

        <v-btn
          type="submit"
          color="secondary"
          variant="flat"
          block
          size="large"
          :loading="loading"
        >
          Войти
        </v-btn>

        <v-alert v-if="error" type="error" variant="tonal" class="mt-4">
          {{ error }}
        </v-alert>
      </v-form>
    </v-card>

    <div class="text-center mt-6 text-secondary anim-fade-up delay-2">
      <p>Для входа используйте email администратора</p>
      <p class="text-xs">После входа потребуется двухфакторная аутентификация</p>
    </div>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { loginAdmin, send2FACode } from '../store/admin.js'

const router = useRouter()
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  if (!email.value || !password.value) {
    error.value = 'Заполните все поля'
    return
  }

  loading.value = true
  error.value = ''

  try {
    // Пытаемся авторизоваться
    if (loginAdmin(email.value, password.value)) {
      // Отправляем код 2FA
      send2FACode(email.value)
      // Переходим на страницу 2FA верификации
      router.push('/admin/2fa')
    } else {
      error.value = 'Неверные учетные данные'
    }
  } catch (err) {
    error.value = 'Ошибка при входе: ' + err.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.anim-fade-up {
  animation: fadeUp 0.6s ease-out forwards;
  opacity: 0;
}

.delay-1 {
  animation-delay: 0.1s;
}

.delay-2 {
  animation-delay: 0.2s;
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
