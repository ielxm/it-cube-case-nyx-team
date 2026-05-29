<template>
  <v-container class="py-8" style="max-width: 620px;">
    <h2 class="text-h5 font-weight-bold mb-6">Регистрация команды</h2>

    <!-- Индикатор шагов -->
    <div class="steps-row mb-6">
      <div v-for="(label, i) in ['Кейс', 'Команда', 'Код']" :key="i"
           class="step-item" :class="{ active: step === i+1, done: step > i+1 }">
        <div class="step-circle">
          <v-icon v-if="step > i+1" size="14">mdi-check</v-icon>
          <span v-else>{{ i+1 }}</span>
        </div>
        <span class="step-label">{{ label }}</span>
      </div>
    </div>

    <!-- Шаг 1 -->
    <v-card v-if="step === 1" class="form-card">
      <v-card-title class="px-6 pt-6">Выберите кейс</v-card-title>
      <v-card-text class="px-6">
        <v-radio-group v-model="form.case_id" color="secondary">
          <v-radio v-for="c in cases" :key="c.id" :value="c.id"
                   :disabled="c.registered >= c.limit_teams" class="mb-2">
            <template #label>
              <span>{{ c.title }}
                <span class="text-caption ml-2" style="color: var(--c-text-muted);">({{ c.registered }}/{{ c.limit_teams }})</span>
              </span>
            </template>
          </v-radio>
        </v-radio-group>
      </v-card-text>
      <v-card-actions class="px-6 pb-6">
        <v-btn variant="text" :to="`/events/${slug}`">Назад</v-btn>
        <v-spacer />
        <v-btn color="secondary" variant="flat" :disabled="!form.case_id" @click="step = 2">Далее</v-btn>
      </v-card-actions>
    </v-card>

    <!-- Шаг 2 -->
    <v-card v-if="step === 2" class="form-card">
      <v-card-title class="px-6 pt-6">Данные команды</v-card-title>
      <v-card-text class="px-6">
        <v-text-field v-model="form.name"         label="Название команды" variant="outlined" class="mb-3" />
        <v-text-field v-model="form.captain_name" label="ФИО капитана"     variant="outlined" class="mb-3" />
        <v-text-field v-model="form.email"        label="Email"            variant="outlined" type="email" class="mb-3" />
        <v-text-field v-model="form.phone"        label="Телефон"          variant="outlined" />
      </v-card-text>
      <v-card-actions class="px-6 pb-6">
        <v-btn variant="text" @click="step = 1">Назад</v-btn>
        <v-spacer />
        <v-btn color="secondary" variant="flat" :disabled="!step2Valid" @click="step = 3">Далее</v-btn>
      </v-card-actions>
    </v-card>

    <!-- Шаг 3 -->
    <v-card v-if="step === 3" class="form-card">
      <v-card-title class="px-6 pt-6">Код приглашения</v-card-title>
      <v-card-text class="px-6">
        <p class="mb-4" style="color: var(--c-text-dim);">Введите одноразовый код от организаторов.</p>
        <v-text-field v-model="form.invite_code" label="Код приглашения" variant="outlined" :error-messages="error" />
      </v-card-text>
      <v-card-actions class="px-6 pb-6">
        <v-btn variant="text" @click="step = 2">Назад</v-btn>
        <v-spacer />
        <v-btn color="secondary" variant="flat" :loading="loading" @click="submit">Зарегистрироваться</v-btn>
      </v-card-actions>
    </v-card>

    <!-- Шаг 4: Успех -->
    <v-card v-if="step === 4" class="form-card text-center">
      <v-card-text class="pa-8">
        <v-icon size="72" color="success" class="mb-4">mdi-check-circle-outline</v-icon>
        <h2 class="text-h5 mb-3">Регистрация прошла успешно!</h2>
        <p class="mb-6" style="color: var(--c-text-dim);">Сохраните данные — они показываются только один раз.</p>
        <div class="cred-block pa-5 mb-6 text-left">
          <div class="cred-row mb-3"><span style="color: var(--c-text-dim);">Логин:</span><span class="cred-value">{{ credentials.login }}</span></div>
          <div class="cred-row">         <span style="color: var(--c-text-dim);">Пароль:</span><span class="cred-value">{{ credentials.password }}</span></div>
        </div>
        <v-btn color="secondary" variant="flat" size="large" to="/login">Войти в кабинет</v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api.js'

const route = useRoute()
const slug = route.params.slug
const step = ref(1), cases = ref([]), loading = ref(false), error = ref(''), credentials = ref(null)

const form = ref({
  name: '', captain_name: '', email: '', phone: '',
  case_id: route.query.case_id ? Number(route.query.case_id) : null,
  invite_code: '',
})
const step2Valid = computed(() => form.value.name && form.value.captain_name && form.value.email && form.value.phone)

onMounted(async () => { const res = await api.get(`/events/${slug}`); cases.value = res.data.cases })

async function submit() {
  loading.value = true; error.value = ''
  try { const res = await api.post('/teams/register', form.value); credentials.value = res.data; step.value = 4 }
  catch (e) { error.value = e.response?.data?.detail || 'Ошибка регистрации' }
  finally { loading.value = false }
}
</script>

<style scoped>
.form-card { background: var(--c-card-bg) !important; border: 1px solid var(--c-card-border) !important; }
.steps-row { display: flex; gap: 32px; justify-content: center; }
.step-item { display: flex; flex-direction: column; align-items: center; gap: 6px; opacity: 0.4; transition: opacity 0.2s; }
.step-item.active, .step-item.done { opacity: 1; }
.step-circle { width: 28px; height: 28px; border-radius: 50%; border: 2px solid rgba(109,40,217,0.5); display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: 700; }
.step-item.active .step-circle { background: #6d28d9; border-color: #6d28d9; }
.step-item.done   .step-circle { background: #22c55e; border-color: #22c55e; }
.step-label { font-size: 0.72rem; color: var(--c-text-dim); }
.cred-block { background: var(--c-cred-bg); border: 1px solid var(--c-cred-border); border-radius: 12px; }
.cred-row { display: flex; justify-content: space-between; align-items: center; }
.cred-value { font-family: monospace; font-size: 1.05rem; color: #a78bfa; letter-spacing: 1px; }
</style>
