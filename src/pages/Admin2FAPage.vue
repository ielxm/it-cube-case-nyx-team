<template>
  <div class="admin-2fa-page">

    <section class="hero-section">
      <div class="hero-inner anim-slide-down">
        <v-icon color="#b8b8d0" size="40" class="mb-3">mdi-shield-check</v-icon>
        <span class="hero-logo-text">NYX</span>
        <span class="hero-logo-tagline">Двухфакторная аутентификация</span>
      </div>
    </section>

    <div class="form-wrap">
      <v-card class="admin-card anim-fade-up" :elevation="0" max-width="420" width="100%">
        <v-card-text class="pa-6">
          <h2 class="card-title mb-1">Подтверждение входа</h2>
          <p class="card-sub mb-1">
            Код отправлен на <strong>{{ admin?.email }}</strong>
          </p>
          <p class="card-sub mb-5" style="color: var(--c-text-muted);">
            Проверьте почту — код действителен 5 минут
          </p>

          <v-form @submit.prevent="handleVerify">
            <v-otp-input
              v-model="code"
              length="6"
              type="number"
              variant="outlined"
              class="justify-center mb-5"
            />

            <v-btn
              type="submit"
              color="secondary"
              variant="flat"
              block
              size="large"
              rounded="sm"
              :loading="loading"
            >
              Подтвердить
            </v-btn>

            <v-alert v-if="error" type="error" variant="tonal" density="compact" class="mt-4">
              {{ error }}
            </v-alert>

            <v-divider class="my-5" />

            <div class="text-center">
              <p class="card-sub mb-2">Код не пришёл?</p>
              <v-btn
                variant="text"
                size="small"
                color="secondary"
                :loading="resendLoading"
                :disabled="resendCountdown > 0"
                @click="resendCode"
              >
                {{ resendCountdown > 0 ? `Отправить через ${resendCountdown}с` : 'Отправить заново' }}
              </v-btn>
            </div>
          </v-form>
        </v-card-text>
      </v-card>

      <v-btn variant="text" size="small" to="/admin/login" class="hint-text anim-fade-up delay-2">
        ← Вернуться к входу
      </v-btn>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { admin, pendingToken, verifyTOTP, resendTOTP } from '../store/admin.js'

const router         = useRouter()
const code           = ref('')
const loading        = ref(false)
const error          = ref('')
const resendLoading  = ref(false)
const resendCountdown = ref(0)

onMounted(() => {
  if (!pendingToken.value && !admin.value) {
    router.push('/admin/login')
  }
})

async function handleVerify() {
  if (code.value.length !== 6) {
    error.value = 'Введите 6-значный код'
    return
  }
  loading.value = true
  error.value   = ''
  try {
    await verifyTOTP(code.value)
    router.push('/admin/dashboard')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Неверный или истёкший код'
  } finally {
    loading.value = false
  }
}

async function resendCode() {
  resendLoading.value   = true
  resendCountdown.value = 60
  try {
    await resendTOTP()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка при повторной отправке'
  } finally {
    resendLoading.value = false
  }
  const interval = setInterval(() => {
    resendCountdown.value--
    if (resendCountdown.value <= 0) clearInterval(interval)
  }, 1000)
}
</script>

<style scoped>
.admin-2fa-page {
  min-height: 100vh;
  background: var(--c-page-bg);
  display: flex;
  flex-direction: column;
}

.hero-section {
  background: linear-gradient(180deg, #2e2e42 0%, #1e1e2e 100%);
  border-bottom: 2px solid #111120;
  padding: 36px 20px 28px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.45);
}

.hero-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.hero-logo-text {
  font-family: 'PT Serif', Georgia, serif;
  font-size: 42px;
  font-weight: 700;
  color: #e8e8f4;
  letter-spacing: 12px;
  line-height: 1;
  text-shadow: 1px 1px 0 rgba(0,0,0,0.6), 0 0 24px rgba(140,140,230,0.22);
}

.hero-logo-tagline {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 10px;
  font-weight: 600;
  color: #6868a0;
  letter-spacing: 3px;
  text-transform: uppercase;
  margin-top: 2px;
}

.form-wrap {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px 16px;
  gap: 14px;
}

.admin-card {
  background: var(--c-card-bg) !important;
  border: 1px solid var(--c-card-border) !important;
  border-radius: 4px !important;
  transition: border-color 0.25s, box-shadow 0.25s;
}

.card-title {
  font-family: 'PT Serif', Georgia, Times, serif;
  font-size: 17px;
  font-weight: 700;
  color: #1a1a28;
}

.card-sub {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 12px;
  color: var(--c-text-dim);
}

.hint-text {
  font-size: 11px;
  color: var(--c-text-muted);
}
</style>
