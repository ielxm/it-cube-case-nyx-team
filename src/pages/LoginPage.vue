<template>
  <v-container class="py-12" style="max-width: 420px;">

    <div class="text-center mb-8 anim-fade-up">
      <v-icon size="52" color="secondary" class="mb-3">mdi-account-circle-outline</v-icon>
      <h1 class="text-h5 font-weight-bold">Вход в кабинет</h1>
      <p class="mt-1" style="color: var(--c-text-dim);">Введите данные, полученные при регистрации</p>
    </div>

    <v-card class="form-card pa-6 anim-fade-up delay-1">
      <v-text-field v-model="form.login" label="Логин" variant="outlined"
                    prepend-inner-icon="mdi-account" class="mb-4" />
      <v-text-field v-model="form.password" label="Пароль" type="password"
                    variant="outlined" prepend-inner-icon="mdi-lock"
                    :error-messages="error" @keyup.enter="submit" />

      <v-btn color="secondary" variant="flat" block size="large" class="mt-5 submit-btn"
             :loading="loading" @click="submit">
        Войти
      </v-btn>

      <div class="text-center mt-5">
        <span style="color: var(--c-text-dim); font-size: 0.875rem;">Нет аккаунта? </span>
        <RouterLink to="/signup" class="link-purple">Зарегистрироваться</RouterLink>
      </div>
    </v-card>

  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api.js'
import { login } from '../store/auth.js'

const router  = useRouter()
const loading = ref(false)
const error   = ref('')
const form    = ref({ login: '', password: '' })

async function submit() {
  loading.value = true
  error.value   = ''
  try {
    const res = await api.post('/login', form.value)
    login(res.data)
    router.push('/dashboard')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Неверный логин или пароль'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.form-card {
  background: var(--c-card-bg) !important;
  border: 1px solid var(--c-card-border) !important;
}
.hint-card {
  background: var(--c-hint-bg) !important;
  border: 1px solid var(--c-hint-border) !important;
}
.submit-btn {
  transition: transform 0.15s, box-shadow 0.2s !important;
}
.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(109, 40, 217, 0.4) !important;
}
.hint-val  { color: #a78bfa; font-family: monospace; }
.link-purple { color: #a78bfa; font-size: 0.875rem; }
</style>
