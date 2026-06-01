<template>
  <div class="admin-login-page">

    <section class="hero-section">
      <div class="hero-inner anim-slide-down">
        <v-icon color="#b8b8d0" size="40" class="mb-3">mdi-shield-admin</v-icon>
        <span class="hero-logo-text">NYX</span>
        <span class="hero-logo-tagline">Панель администратора</span>
      </div>
    </section>

    <div class="form-wrap">
      <v-card class="admin-card anim-fade-up" :elevation="0" max-width="400" width="100%">
        <v-card-text class="pa-6">
          <h2 class="card-title mb-1">Вход</h2>
          <p class="card-sub mb-5">Введите учётные данные администратора</p>

          <v-form @submit.prevent="handleLogin">
            <v-text-field
              v-model="email"
              label="Email администратора"
              type="email"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-email-outline"
              class="mb-3"
              :disabled="loading"
              required
            />
            <v-text-field
              v-model="password"
              label="Пароль"
              type="password"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-lock-outline"
              class="mb-4"
              :disabled="loading"
              required
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
              Войти
            </v-btn>

            <v-alert v-if="error" type="error" variant="tonal" density="compact" class="mt-4">
              {{ error }}
            </v-alert>
          </v-form>
        </v-card-text>
      </v-card>

      <p class="hint-text anim-fade-up delay-2">
        После входа будет отправлен код подтверждения на email
      </p>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { loginAdmin } from '../store/admin.js'

const router   = useRouter()
const email    = ref('')
const password = ref('')
const loading  = ref(false)
const error    = ref('')

async function handleLogin() {
  if (!email.value || !password.value) {
    error.value = 'Заполните все поля'
    return
  }
  loading.value = true
  error.value   = ''
  try {
    await loginAdmin(email.value, password.value)
    router.push('/admin/2fa')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Неверный email или пароль'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.admin-login-page {
  min-height: 100vh;
  background: var(--c-page-bg);
  display: flex;
  flex-direction: column;
}

/* Hero — same dark gradient as main page hero */
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
  letter-spacing: 5px;
  text-transform: uppercase;
  margin-top: 2px;
}

/* Form area */
.form-wrap {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px 16px;
  gap: 14px;
}

/* Card — same as home-card / case-card */
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
  font-family: Arial, Helvetica, sans-serif;
  font-size: 11px;
  color: var(--c-text-muted);
  text-align: center;
}
</style>
