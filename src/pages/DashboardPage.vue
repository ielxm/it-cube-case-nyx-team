<template>
  <v-container class="py-8" style="max-width: 800px;">

    <!-- Не авторизован -->
    <v-card v-if="!team" class="dash-card text-center pa-10 anim-fade-up">
      <v-icon size="64" color="secondary" class="mb-4">mdi-lock-outline</v-icon>
      <h2 class="text-h6 mb-2">Доступ закрыт</h2>
      <p class="text-secondary mb-5">Войдите в аккаунт, чтобы открыть личный кабинет</p>
      <v-btn color="secondary" variant="flat" to="/login">Войти</v-btn>
    </v-card>

    <!-- Кабинет -->
    <div v-else>

      <div class="d-flex align-center mb-1 anim-fade-up">
        <v-icon color="secondary" class="mr-2">mdi-view-dashboard-outline</v-icon>
        <h1 class="text-h5 font-weight-bold">Личный кабинет</h1>
      </div>
      <p class="text-secondary mb-6 anim-fade-up delay-1">{{ teamData?.event_title }}</p>

      <v-tabs v-model="tab" color="secondary" class="mb-6 anim-fade-up delay-2">
        <v-tab value="team">Команда</v-tab>
        <v-tab value="case">Мой кейс</v-tab>
        <v-tab value="switch">Сменить кейс</v-tab>
      </v-tabs>

      <v-window v-model="tab">

        <!-- ─── Вкладка: Команда ─── -->
        <v-window-item value="team">
          <v-card class="dash-card mb-4">
            <v-card-title class="px-6 pt-5">
              <v-icon class="mr-2" color="secondary">mdi-account-group</v-icon>
              {{ teamData?.name }}
            </v-card-title>
            <v-card-text class="px-6">
              <v-row>
                <v-col cols="12" sm="6">
                  <div class="info-item">
                    <span class="info-label">Капитан</span>
                    <span>{{ teamData?.captain_name }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Email</span>
                    <span>{{ teamData?.email }}</span>
                  </div>
                </v-col>
                <v-col cols="12" sm="6">
                  <div class="info-item">
                    <span class="info-label">Телефон</span>
                    <span>{{ teamData?.phone }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Текущий кейс</span>
                    <v-chip color="secondary" variant="tonal" size="small">{{ teamData?.case_title }}</v-chip>
                  </div>
                </v-col>
              </v-row>
            </v-card-text>
            <v-card-actions class="px-6 pb-5">
              <v-btn :color="editMode ? 'error' : 'secondary'" variant="text"
                     :prepend-icon="editMode ? 'mdi-close' : 'mdi-pencil'"
                     @click="toggleEdit">
                {{ editMode ? 'Отмена' : 'Редактировать' }}
              </v-btn>
            </v-card-actions>
          </v-card>

          <!-- Форма редактирования — появляется с анимацией -->
          <Transition name="expand">
            <v-card v-if="editMode" class="dash-card">
              <v-card-title class="px-6 pt-5">Редактирование</v-card-title>
              <v-card-text class="px-6">
                <v-row>
                  <v-col cols="12" sm="6">
                    <v-text-field v-model="editForm.name"         label="Название команды" variant="outlined" />
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field v-model="editForm.captain_name" label="ФИО капитана"     variant="outlined" />
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field v-model="editForm.email"        label="Email"            variant="outlined" type="email" />
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field v-model="editForm.phone"        label="Телефон"          variant="outlined" />
                  </v-col>
                </v-row>
              </v-card-text>
              <v-card-actions class="px-6 pb-5">
                <v-spacer />
                <v-btn color="secondary" variant="flat" :loading="saving" @click="save">Сохранить</v-btn>
              </v-card-actions>
            </v-card>
          </Transition>
        </v-window-item>

        <!-- ─── Вкладка: Мой кейс ─── -->
        <v-window-item value="case">
          <v-card class="dash-card">
            <v-card-title class="px-6 pt-5">
              <v-icon class="mr-2" color="secondary">mdi-briefcase-outline</v-icon>
              {{ teamData?.case_title }}
            </v-card-title>
            <v-card-text class="px-6">
              <p style="line-height: 1.7; color: rgba(255,255,255,0.75);">
                {{ teamData?.case_description }}
              </p>

              <v-divider class="my-5" />

              <h3 class="text-body-1 font-weight-bold mb-3">Что нужно сдать:</h3>
              <v-list bg-color="transparent" density="compact">
                <v-list-item
                  v-for="(item, i) in deliverables" :key="item"
                  :title="item"
                  prepend-icon="mdi-checkbox-blank-circle-outline"
                  class="px-0 deliverable-item"
                  :style="`animation-delay: ${i * 0.08}s`"
                />
              </v-list>

              <v-divider class="my-5" />

              <h3 class="text-body-1 font-weight-bold mb-3">Полезные ресурсы:</h3>
              <div class="d-flex flex-wrap gap-2">
                <v-chip
                  v-for="(res, i) in resources" :key="res.label"
                  variant="outlined" color="secondary" size="small"
                  prepend-icon="mdi-link-variant"
                  class="resource-chip"
                  :style="`animation-delay: ${i * 0.07}s`"
                >
                  {{ res.label }}
                </v-chip>
              </div>
            </v-card-text>
          </v-card>
        </v-window-item>

        <!-- ─── Вкладка: Сменить кейс ─── -->
        <v-window-item value="switch">
          <p class="mb-4" style="margin-top:0; color: var(--c-text-dim);">Вы можете сменить кейс, если в нём есть свободные места.</p>

          <div v-if="loadingCases" class="text-center py-8">
            <v-progress-circular indeterminate color="secondary" />
          </div>

          <v-row v-else>
            <v-col
              v-for="(c, i) in allCases" :key="c.id"
              cols="12" md="6"
              :class="`anim-fade-up delay-${i + 1}`"
            >
              <v-card class="dash-card"
                      :style="c.id === teamData?.case_id ? 'border-color: rgba(167,139,250,0.6) !important;' : ''">
                <v-card-title class="px-5 pt-4 text-body-1 font-weight-bold">{{ c.title }}</v-card-title>
                <v-card-text class="px-5">
                  <v-progress-linear
                    :model-value="(c.registered / c.limit_teams) * 100"
                    color="secondary" bg-color="rgba(255,255,255,0.07)"
                    rounded height="5" class="mb-1"
                  />
                  <span class="spots-text">{{ c.registered }} / {{ c.limit_teams }} команд</span>
                </v-card-text>
                <v-card-actions class="px-5 pb-4">
                  <v-chip v-if="c.id === teamData?.case_id" color="secondary" variant="tonal" size="small">
                    Текущий кейс
                  </v-chip>
                  <v-btn v-else color="secondary" variant="text" size="small"
                         :disabled="c.registered >= c.limit_teams"
                         :loading="switchingTo === c.id"
                         @click="switchCase(c.id)">
                    {{ c.registered < c.limit_teams ? 'Выбрать' : 'Мест нет' }}
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
        </v-window-item>

      </v-window>

      <v-snackbar v-model="savedSnack" color="success" timeout="3000">
        <v-icon class="mr-2">mdi-check</v-icon> Данные успешно сохранены!
      </v-snackbar>
    </div>

  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api.js'
import { team, login } from '../store/auth.js'

const tab          = ref('team')
const teamData     = ref(null)
const editMode     = ref(false)
const saving       = ref(false)
const savedSnack   = ref(false)
const allCases     = ref([])
const loadingCases = ref(false)
const switchingTo  = ref(null)
const editForm     = ref({ name: '', captain_name: '', email: '', phone: '' })

const deliverables = [
  'Репозиторий с исходным кодом (GitHub/GitLab)',
  'Рабочее демо (деплой или локальный запуск)',
  'Презентация проекта (PDF, до 15 слайдов)',
  'README с инструкцией по запуску',
]
const resources = [
  { label: 'Vue 3 Docs' }, { label: 'FastAPI Docs' },
  { label: 'Vuetify 3' },  { label: 'SQLite Tutorial' },
]

onMounted(async () => {
  if (!team.value) return
  // Сразу показываем сохранённые данные, чтобы страница не была пустой после обновления
  const cached = JSON.parse(localStorage.getItem('teamData') || 'null')
  if (cached) {
    teamData.value = cached
    fillEditForm(cached)
    if (cached.event_slug) loadCases(cached.event_slug)
  }
  try {
    const res = await api.get(`/teams/${team.value.id}`)
    teamData.value = res.data
    fillEditForm(res.data)
    localStorage.setItem('teamData', JSON.stringify(res.data))
    loadCases(res.data.event_slug)
  } catch {
    // Оставляем кешированные данные
  }
})

async function loadCases(eventSlug) {
  loadingCases.value = true
  const res = await api.get(`/events/${eventSlug}`)
  allCases.value = res.data.cases
  loadingCases.value = false
}

function fillEditForm(data) {
  editForm.value = { name: data.name, captain_name: data.captain_name, email: data.email, phone: data.phone }
}

function toggleEdit() {
  editMode.value = !editMode.value
  if (editMode.value) fillEditForm(teamData.value)
}

async function save() {
  saving.value = true
  try {
    await api.put(`/teams/${team.value.id}`, editForm.value)
    teamData.value = { ...teamData.value, ...editForm.value }
    login({ ...team.value, ...editForm.value })
    editMode.value = false
    savedSnack.value = true
  } finally {
    saving.value = false
  }
}

async function switchCase(caseId) {
  switchingTo.value = caseId
  try {
    await api.put(`/teams/${team.value.id}`, { ...editForm.value, case_id: caseId })
    const res = await api.get(`/teams/${team.value.id}`)
    teamData.value = res.data
    fillEditForm(res.data)
    await loadCases(res.data.event_slug)
    savedSnack.value = true
  } finally {
    switchingTo.value = null
  }
}
</script>

<style scoped>
.dash-card {
  background: #110e24 !important;
  border: 1px solid rgba(109, 40, 217, 0.25) !important;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.dash-card:hover {
  box-shadow: 0 0 20px rgba(109, 40, 217, 0.1) !important;
}

.info-item { display: flex; flex-direction: column; margin-bottom: 18px; }
.info-label {
  font-size: 0.7rem;
  color: rgba(255,255,255,0.4);
  text-transform: uppercase;
  letter-spacing: 0.8px;
  margin-bottom: 3px;
}

.spots-text { font-size: 0.78rem; color: rgba(255,255,255,0.4); }

/* Анимация появления формы редактирования */
.expand-enter-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.expand-leave-active { transition: opacity 0.2s ease; }
.expand-enter-from { opacity: 0; transform: translateY(-10px); }
.expand-leave-to   { opacity: 0; }

/* Анимация строк чеклиста */
.deliverable-item {
  animation: fadeUp 0.4s ease both;
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateX(-10px); }
  to   { opacity: 1; transform: translateX(0); }
}

/* Анимация чипов ресурсов */
.resource-chip {
  animation: popIn 0.35s ease both;
  transition: transform 0.15s, box-shadow 0.15s;
}
.resource-chip:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(109, 40, 217, 0.25) !important;
}
@keyframes popIn {
  from { opacity: 0; transform: scale(0.8); }
  to   { opacity: 1; transform: scale(1); }
}
</style>
