<template>
  <v-container class="py-8" style="max-width: 400px;">
    <div class="text-center mb-8 anim-fade-up">
      <v-icon size="64" color="secondary" class="mb-4">mdi-shield-check</v-icon>
      <h1 class="text-h4 font-weight-bold mb-2">Двухфакторная аутентификация</h1>
      <p class="text-secondary">Введите код, отправленный на ваш email</p>
    </div>

    <v-card class="dash-card pa-6 anim-fade-up delay-1">
      <v-form @submit.prevent="handleVerify">
        <p class="text-center mb-6">
          <strong>{{ admin?.email }}</strong>
        </p>

        <div class="mb-6">
          <label class="text-secondary mb-2 d-block">Способ верификации</label>
          <v-btn-toggle v-model="method" mandatory divided class="w-100">
            <v-btn value="email" icon="mdi-email">Email</v-btn>
            <v-btn value="sms" icon="mdi-phone">SMS</v-btn>
          </v-btn-toggle>
        </div>

        <v-otp-input
          v-model="code"
          length="6"
          type="number"
          variant="outlined"
          class="justify-center mb-4"
        />

        <v-btn
          type="submit"
          color="secondary"
          variant="flat"
          block
          size="large"
          :loading="loading"
        >
          Подтвердить
        </v-btn>

        <v-alert v-if="error" type="error" variant="tonal" class="mt-4">
          {{ error }}
        </v-alert>

        <v-divider class="my-4" />

        <div class="text-center">
          <p class="text-secondary text-sm mb-2">Код не пришел?</p>
          <v-btn
            variant="text"
            size="small"
            @click="resendCode"
            :loading="resendLoading"
            :disabled="resendCountdown > 0"
          >
            {{ resendCountdown > 0 ? `Отправить через ${resendCountdown}с` : 'Отправить заново' }}
          </v-btn>
        </div>
      </v-form>

      <v-alert type="info" variant="tonal" class="mt-4">
        <v-icon size="sm" class="mr-2">mdi-information</v-icon>
        <span class="text-sm">Для демонстрации, любой 6-значный код сработает</span>
      </v-alert>
    </v-card>

    <div class="text-center mt-6">
      <v-btn variant="text" size="small" to="/admin/login">Вернуться на вход</v-btn>
    </div>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { admin, verify2FA } from '../store/admin.js'

const router = useRouter()
const code = ref('')
const method = ref('email')
const loading = ref(false)
const error = ref('')
const resendLoading = ref(false)
const resendCountdown = ref(0)

if (!admin.value) {
  router.push('/admin/login')
}

async function handleVerify() {
  if (code.value.length !== 6) {
    error.value = 'Введите 6-значный код'
    return
  }

  loading.value = true
  error.value = ''

  try {
    if (verify2FA(code.value)) {
      // Успешная верификация
      router.push('/admin/dashboard')
    } else {
      error.value = 'Неверный код. Попробуйте еще раз'
    }
  } catch (err) {
    error.value = 'Ошибка при верификации: ' + err.message
  } finally {
    loading.value = false
  }
}

async function resendCode() {
  resendLoading.value = true
  resendCountdown.value = 60

  // Генерируем новый код
  const newCode = Math.floor(100000 + Math.random() * 900000)
  localStorage.setItem('admin2FACode', newCode.toString())
  console.log(`2FA Code (${method.value}):`, newCode)

  const interval = setInterval(() => {
    resendCountdown.value--
    if (resendCountdown.value <= 0) {
      clearInterval(interval)
      resendLoading.value = false
    }
  }, 1000)
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
