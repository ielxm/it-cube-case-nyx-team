<template>
  <v-container class="py-8" style="max-width: 620px;">

    
    <v-card v-if="!user" class="form-card text-center pa-10">
      <v-icon size="56" color="secondary" class="mb-4">mdi-lock-outline</v-icon>
      <h2 class="text-h6 mb-3" style="color:#1a1a2e;">Требуется авторизация</h2>
      <p class="mb-6" style="color: var(--c-text-dim);">Войдите в аккаунт, чтобы создать команду</p>
      <v-btn color="secondary" variant="flat" to="/login">Войти</v-btn>
      <div class="mt-4">
        <span style="color: var(--c-text-dim); font-size: 0.875rem;">Нет аккаунта? </span>
        <RouterLink to="/signup" class="link-accent">Зарегистрироваться</RouterLink>
      </div>
    </v-card>

    <template v-else>
      <h2 class="text-h5 font-weight-bold mb-6">Создать команду</h2>

      
      <div class="steps-row mb-6">
        <div v-for="(label, i) in ['Команда', 'Кейс', 'Код']" :key="i"
             class="step-item" :class="{ active: step === i+1, done: step > i+1 }">
          <div class="step-circle">
            <v-icon v-if="step > i+1" size="14">mdi-check</v-icon>
            <span v-else>{{ i+1 }}</span>
          </div>
          <span class="step-label">{{ label }}</span>
        </div>
      </div>

      
      <v-card v-if="step === 1" class="form-card">
        <v-card-title class="px-6 pt-6" style="color:#1a1a2e;">Название команды</v-card-title>
        <v-card-text class="px-6">
          <v-text-field v-model="form.name" label="Название команды" variant="outlined" class="mb-3" />
          <p v-if="event" style="color: var(--c-text-dim); font-size: 0.875rem;">
            Мероприятие: <strong>{{ event.title }}</strong>
          </p>
          <p style="color: var(--c-text-dim); font-size: 0.875rem;">
            Лидер: <strong>{{ user.full_name }}</strong>
          </p>
        </v-card-text>
        <v-card-actions class="px-6 pb-6">
          <v-btn variant="text" :to="`/events/${slug}`">Назад</v-btn>
          <v-spacer />
          <v-btn color="secondary" variant="flat" :disabled="!form.name.trim()" @click="step = 2">Далее</v-btn>
        </v-card-actions>
      </v-card>

      
      <v-card v-if="step === 2" class="form-card">
        <v-card-title class="px-6 pt-6" style="color:#1a1a2e;">Выберите кейс</v-card-title>
        <v-card-text class="px-6">
          <v-radio-group v-model="form.case_id" color="secondary">
            <v-radio v-for="c in cases" :key="c.id" :value="c.id"
                     :disabled="c.registered >= c.limit_teams" class="mb-2">
              <template #label>
                <span>{{ c.title }}
                  <span class="text-caption ml-2" style="color: var(--c-text-muted);">
                    ({{ c.registered }}/{{ c.limit_teams }})
                  </span>
                </span>
              </template>
            </v-radio>
          </v-radio-group>
        </v-card-text>
        <v-card-actions class="px-6 pb-6">
          <v-btn variant="text" @click="step = 1">Назад</v-btn>
          <v-spacer />
          <v-btn color="secondary" variant="flat" :disabled="!form.case_id" @click="step = 3">Далее</v-btn>
        </v-card-actions>
      </v-card>

      
      <v-card v-if="step === 3" class="form-card">
        <v-card-title class="px-6 pt-6" style="color:#1a1a2e;">Код приглашения</v-card-title>
        <v-card-text class="px-6">
          <p class="mb-4" style="color: var(--c-text-dim);">Введите одноразовый код от организаторов мероприятия.</p>
          <v-text-field v-model="form.invite_code" label="Код приглашения" variant="outlined"
                        :error-messages="error" />
        </v-card-text>
        <v-card-actions class="px-6 pb-6">
          <v-btn variant="text" @click="step = 2">Назад</v-btn>
          <v-spacer />
          <v-btn color="secondary" variant="flat" :loading="loading"
                 :disabled="!form.invite_code.trim()" @click="submit">
            Создать команду
          </v-btn>
        </v-card-actions>
      </v-card>

      
      <v-card v-if="step === 4" class="form-card text-center">
        <v-card-text class="pa-8">
          <v-icon size="72" color="success" class="mb-4">mdi-check-circle-outline</v-icon>
          <h2 class="text-h5 mb-3" style="color:#1a1a2e;">Команда создана!</h2>
          <p class="mb-2" style="color: var(--c-text-dim);">Передайте код участникам — они смогут вступить в команду по нему.</p>
          <p class="mb-6" style="color: var(--c-text-dim);">Код также доступен в личном кабинете.</p>
          <div class="cred-block pa-5 mb-6 text-left">
            <div class="cred-row mb-3">
              <span style="color: var(--c-text-dim);">Команда:</span>
              <span class="cred-value">{{ form.name }}</span>
            </div>
            <div class="cred-row">
              <span style="color: var(--c-text-dim);">Код команды:</span>
              <span class="cred-value">{{ teamCode }}</span>
            </div>
          </div>
          <v-btn color="secondary" variant="flat" size="large" to="/dashboard">Перейти в кабинет</v-btn>
        </v-card-text>
      </v-card>
    </template>

  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api.js'
import { user } from '../store/auth.js'

const route = useRoute()
const slug  = route.params.slug

const step    = ref(1)
const cases   = ref([])
const event   = ref(null)
const loading = ref(false)
const error   = ref('')
const teamCode = ref('')

const form = ref({ name: '', case_id: null, invite_code: '' })

onMounted(async () => {
  try {
    const res = await api.get(`/events/${slug}`)
    event.value = res.data
    cases.value = res.data.cases
    const qCaseId = Number(route.query.case_id)
    if (qCaseId) form.value.case_id = qCaseId
  } catch {  }
})

async function submit() {
  loading.value = true
  error.value   = ''
  try {
    const res = await api.post('/teams', {
      name:               form.value.name,
      event_id:           event.value.id,
      case_id:            form.value.case_id,
      event_invite_code:  form.value.invite_code,
      user_id:            user.value.id,
    })
    teamCode.value = res.data.team_code
    step.value = 4
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка создания команды'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.form-card {
  background: var(--c-card-bg) !important;
  border: 1px solid var(--c-card-border) !important;
  border-radius: 4px !important;
  box-shadow: 2px 2px 6px rgba(0,0,0,0.10) !important;
}
.steps-row { display: flex; gap: 32px; justify-content: center; }
.step-item  { display: flex; flex-direction: column; align-items: center; gap: 6px; opacity: 0.4; transition: opacity 0.2s; }
.step-item.active, .step-item.done { opacity: 1; }
.step-circle {
  width: 28px; height: 28px; border-radius: 50%;
  border: 2px solid rgba(26,90,150,0.4);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.8rem; font-weight: 700; color: #1a1a2e;
}
.step-item.active .step-circle { background: #1a5a96; border-color: #1a5a96; color: #fff; }
.step-item.done   .step-circle { background: #2e7d32; border-color: #2e7d32; color: #fff; }
.step-label { font-size: 0.72rem; color: var(--c-text-dim); }
.cred-block { background: var(--c-cred-bg); border: 1px solid var(--c-cred-border); border-radius: 6px; }
.cred-row   { display: flex; justify-content: space-between; align-items: center; }
.cred-value { font-family: monospace; font-size: 1.05rem; color: #1a5a96; letter-spacing: 1px; font-weight: 700; }
.link-accent { color: #a78bfa; font-size: 0.875rem; }
</style>
