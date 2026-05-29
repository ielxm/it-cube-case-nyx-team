<template>
  <v-container class="py-10" style="max-width: 480px;">

    <!-- Заголовок -->
    <div class="text-center mb-8 anim-fade-up">
      <v-icon size="52" color="secondary" class="mb-3">mdi-account-plus-outline</v-icon>
      <h1 class="text-h5 font-weight-bold">Создать аккаунт</h1>
      <p class="mt-1" style="color: var(--c-text-dim);">Зарегистрируйтесь, чтобы участвовать в мероприятиях</p>
    </div>

    <!-- Карточка формы -->
    <v-card class="form-card pa-6 anim-fade-up delay-1" v-if="!success">

      <!-- Переключатель: Email / Телефон -->
      <div class="method-tabs mb-5">
        <button class="method-btn" :class="{ active: method === 'email' }" @click="method = 'email'">
          <v-icon size="18" class="mr-1">mdi-gmail</v-icon> Email
        </button>
        <button class="method-btn" :class="{ active: method === 'phone' }" @click="method = 'phone'">
          <v-icon size="18" class="mr-1">mdi-phone</v-icon> Телефон
        </button>
      </div>

      <!-- Поля формы -->
      <v-text-field
        v-model="form.full_name"
        label="ФИО"
        variant="outlined"
        prepend-inner-icon="mdi-account"
        class="mb-3"
        placeholder="Иванов Иван Иванович"
      />

      <v-text-field
        v-model="form.age"
        label="Возраст"
        variant="outlined"
        prepend-inner-icon="mdi-cake-variant"
        type="number"
        class="mb-3"
        :rules="[v => v >= 10 && v <= 99 || 'Укажите корректный возраст']"
      />

      <!-- Email или телефон в зависимости от выбора -->
      <Transition name="field-switch" mode="out-in">
        <v-text-field
          v-if="method === 'email'"
          key="email"
          v-model="form.email"
          label="Email (Gmail)"
          variant="outlined"
          prepend-inner-icon="mdi-email-outline"
          type="email"
          class="mb-3"
          placeholder="example@gmail.com"
        />
        <v-text-field
          v-else
          key="phone"
          v-model="form.phone"
          label="Номер телефона"
          variant="outlined"
          prepend-inner-icon="mdi-phone-outline"
          class="mb-3"
          placeholder="+7 900 000-00-00"
        />
      </Transition>

      <v-text-field
        v-model="form.password"
        label="Пароль"
        variant="outlined"
        prepend-inner-icon="mdi-lock-outline"
        :type="showPass ? 'text' : 'password'"
        :append-inner-icon="showPass ? 'mdi-eye-off' : 'mdi-eye'"
        @click:append-inner="showPass = !showPass"
      />

      <v-alert v-if="error" type="error" variant="tonal" density="compact" class="mb-2 mt-1">
        {{ error }}
      </v-alert>

      <v-btn
        color="secondary" variant="flat" block size="large"
        class="mt-4 submit-btn" :loading="loading" @click="submit"
      >
        Зарегистрироваться
      </v-btn>

      <div class="text-center mt-4">
        <span style="color: var(--c-text-dim); font-size: 0.875rem;">Уже есть аккаунт? </span>
        <RouterLink to="/login" class="link-purple">Войти</RouterLink>
      </div>

    </v-card>

    <!-- Успешная регистрация -->
    <v-card v-else class="form-card pa-8 text-center anim-fade-up">
      <v-icon size="72" color="success" class="mb-4">mdi-check-circle-outline</v-icon>
      <h2 class="text-h5 mb-3">Добро пожаловать!</h2>
      <p style="color: var(--c-text-dim);" class="mb-2">Ваш логин для входа:</p>
      <div class="cred-block pa-4 mb-6">
        <span class="cred-value">{{ createdLogin }}</span>
      </div>
      <p style="color: var(--c-text-dim); font-size: 0.85rem;" class="mb-5">
        Сохраните логин — он понадобится для входа вместе с паролем.
      </p>
      <v-btn color="secondary" variant="flat" to="/login">Войти в аккаунт</v-btn>
    </v-card>

  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api.js'

const method   = ref('email')
const loading  = ref(false)
const error    = ref('')
const success  = ref(false)
const showPass = ref(false)
const createdLogin = ref('')

const form = ref({
  full_name: '',
  age: '',
  email: '',
  phone: '',
  password: '',
})

async function submit() {
  error.value = ''

  // Простая проверка заполненности
  if (!form.value.full_name || !form.value.age || !form.value.password) {
    error.value = 'Заполните все поля'
    return
  }
  if (method.value === 'email' && !form.value.email) {
    error.value = 'Введите email'
    return
  }
  if (method.value === 'phone' && !form.value.phone) {
    error.value = 'Введите телефон'
    return
  }

  loading.value = true
  try {
    const res = await api.post('/users/register', {
      full_name: form.value.full_name,
      age:       Number(form.value.age),
      email:     method.value === 'email' ? form.value.email : null,
      phone:     method.value === 'phone' ? form.value.phone : null,
      password:  form.value.password,
    })
    createdLogin.value = res.data.login
    success.value = true
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка регистрации'
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

/* Переключатель Email / Телефон */
.method-tabs {
  display: flex;
  background: var(--c-hint-bg);
  border: 1px solid var(--c-hint-border);
  border-radius: 10px;
  padding: 4px;
  gap: 4px;
}
.method-btn {
  flex: 1;
  padding: 8px 0;
  border: none;
  border-radius: 7px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--c-text-dim);
  background: transparent;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.method-btn.active {
  background: #6d28d9;
  color: #fff;
  box-shadow: 0 2px 8px rgba(109, 40, 217, 0.4);
}

/* Анимация смены поля email/телефон */
.field-switch-enter-active, .field-switch-leave-active { transition: opacity 0.2s, transform 0.2s; }
.field-switch-enter-from { opacity: 0; transform: translateX(10px); }
.field-switch-leave-to   { opacity: 0; transform: translateX(-10px); }

.submit-btn {
  transition: transform 0.15s, box-shadow 0.2s !important;
}
.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(109, 40, 217, 0.4) !important;
}

.cred-block {
  background: var(--c-cred-bg);
  border: 1px solid var(--c-cred-border);
  border-radius: 10px;
  display: inline-block;
}
.cred-value { font-family: monospace; font-size: 1.2rem; color: #a78bfa; letter-spacing: 1px; }
.link-purple { color: #a78bfa; font-size: 0.875rem; }
</style>
