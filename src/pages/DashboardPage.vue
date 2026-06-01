<template>
  <v-container class="py-8" style="max-width: 820px;">

    <v-card v-if="!user" class="dash-card text-center pa-10">
      <v-icon size="56" color="#3a3a78" class="mb-4">mdi-lock-outline</v-icon>
      <h2 class="text-h6 mb-2" style="color:#1a1a2e;">Доступ закрыт</h2>
      <p class="mb-5" style="color: var(--c-text-dim);">Войдите в аккаунт, чтобы открыть личный кабинет</p>
      <v-btn color="#3a3a78" variant="flat" to="/login">Войти</v-btn>
    </v-card>

    <div v-else>
      
      <div class="d-flex align-center justify-space-between mb-6 flex-wrap gap-3">
        <div class="d-flex align-center">
          <v-icon color="#3a3a78" class="mr-2">mdi-view-dashboard-outline</v-icon>
          <div>
            <h1 class="text-h5 font-weight-bold" style="color:#1a1a2e;">Личный кабинет</h1>
            <p class="text-caption" style="color: var(--c-text-dim);">{{ user.full_name }} · @{{ user.login }}</p>
          </div>
        </div>
        <v-btn color="#3a3a78" variant="flat" prepend-icon="mdi-calendar-star" to="/">
          Выбрать мероприятие
        </v-btn>
      </div>

      <v-tabs v-model="tab" color="#3a3a78" class="mb-6" bg-color="transparent" slider-color="#3a3a78">
        <v-tab value="teams">Мои команды</v-tab>
        <v-tab value="join">Вступить в команду</v-tab>
      </v-tabs>

      <v-window v-model="tab">

        
        <v-window-item value="teams">
          <v-progress-linear v-if="loading" indeterminate color="#3a3a78" class="mb-4" />

          <div v-if="!loading && !teams.length" class="text-center py-10" style="color: var(--c-text-dim);">
            <v-icon size="48" class="mb-3">mdi-account-group-outline</v-icon>
            <p class="mb-2">Вы пока не состоите ни в одной команде</p>
            <p class="text-caption mb-5">Создайте команду через страницу мероприятия или вступите по коду</p>
            <v-btn color="#3a3a78" variant="flat" to="/">Выбрать мероприятие</v-btn>
          </div>

          <v-row v-else>
            <v-col v-for="t in teams" :key="t.id" cols="12">
              <v-card class="dash-card">

                <v-card-title class="px-6 pt-5 d-flex align-center justify-space-between flex-wrap gap-2">
                  <span style="color:#1a1a2e;">
                    <v-icon class="mr-1" color="#3a3a78">mdi-account-group</v-icon>
                    {{ t.name }}
                  </span>
                  <v-chip :color="t.is_leader ? '#3a3a78' : 'grey'" variant="tonal" size="small">
                    {{ t.is_leader ? 'Лидер' : 'Участник' }}
                  </v-chip>
                </v-card-title>

                <v-card-text class="px-6">
                  <v-row>
                    <v-col cols="12" sm="6">
                      <div class="info-item">
                        <span class="info-label">Мероприятие</span>
                        <span class="info-val">{{ t.event_title }}</span>
                      </div>
                      <div class="info-item">
                        <span class="info-label">Кейс</span>
                        <span class="info-val">{{ t.case_title || '—' }}</span>
                      </div>
                    </v-col>
                    <v-col cols="12" sm="6">
                      <div class="info-item">
                        <span class="info-label">Участники</span>
                        <div class="members-list mt-1">
                          <div v-for="m in t.members" :key="m.id" class="member-row">
                            <v-icon size="14" color="#3a3a78" class="mr-1">mdi-account-outline</v-icon>
                            <span class="info-val">{{ m.full_name }}</span>
                            <v-chip v-if="m.is_leader" class="ml-2" color="#3a3a78" variant="tonal" size="x-small">Лидер</v-chip>
                          </div>
                        </div>
                      </div>
                      <div v-if="t.is_leader" class="info-item">
                        <span class="info-label">Код команды</span>
                        <div class="d-flex align-center gap-1 mt-1">
                          <code class="team-code">{{ t.team_code }}</code>
                          <v-btn icon size="x-small" variant="text" @click="copyCode(t.team_code)">
                            <v-icon size="15">mdi-content-copy</v-icon>
                          </v-btn>
                        </div>
                      </div>
                    </v-col>
                  </v-row>
                </v-card-text>

                <v-card-actions class="px-6 pb-3">
                  <template v-if="t.is_leader">
                    <v-btn size="small" variant="text" color="#3a3a78"
                           :prepend-icon="editingTeam === t.id ? 'mdi-chevron-up' : 'mdi-pencil'"
                           @click="toggleEdit(t)">
                      Название
                    </v-btn>
                    <v-btn size="small" variant="text" color="#3a3a78"
                           :prepend-icon="switchingTeam === t.id ? 'mdi-chevron-up' : 'mdi-swap-horizontal'"
                           @click="toggleSwitch(t)">
                      Сменить кейс
                    </v-btn>
                    <v-spacer />
                    <v-btn size="small" variant="text" color="error" prepend-icon="mdi-trash-can"
                           @click="confirmDelete(t)">
                      Удалить
                    </v-btn>
                  </template>
                  <template v-else>
                    <v-spacer />
                    <v-btn size="small" variant="text" color="error" prepend-icon="mdi-exit-run"
                           @click="leaveTeam(t)">
                      Покинуть
                    </v-btn>
                  </template>
                </v-card-actions>

                
                <Transition name="expand">
                  <div v-if="editingTeam === t.id" class="px-6 pb-5">
                    <v-divider class="mb-4" />
                    <v-text-field v-model="editName" label="Название команды" variant="outlined"
                                  density="compact" hide-details class="mb-3" />
                    <v-btn color="#3a3a78" variant="flat" size="small"
                           :loading="saving" @click="saveName(t)">
                      Сохранить
                    </v-btn>
                  </div>
                </Transition>

                
                <Transition name="expand">
                  <div v-if="switchingTeam === t.id" class="px-6 pb-5">
                    <v-divider class="mb-4" />
                    <div v-if="loadingCases" class="text-center py-4">
                      <v-progress-circular indeterminate color="#3a3a78" size="24" />
                    </div>
                    <div v-else>
                      <v-radio-group v-model="selectedCase" color="secondary">
                        <v-radio v-for="c in eventCases" :key="c.id" :value="c.id"
                                 :disabled="c.id === t.case_id || c.registered >= c.limit_teams">
                          <template #label>
                            <span>{{ c.title }}
                              <span class="text-caption ml-2" style="color: var(--c-text-muted);">
                                ({{ c.registered }}/{{ c.limit_teams }})
                                <span v-if="c.id === t.case_id"> — текущий</span>
                              </span>
                            </span>
                          </template>
                        </v-radio>
                      </v-radio-group>
                      <v-btn color="#3a3a78" variant="flat" size="small"
                             :disabled="!selectedCase || selectedCase === t.case_id"
                             :loading="switchingCase" @click="doSwitchCase(t)">
                        Подтвердить
                      </v-btn>
                    </div>
                  </div>
                </Transition>

              </v-card>
            </v-col>
          </v-row>
        </v-window-item>

        
        <v-window-item value="join">
          <v-card class="dash-card">
            <v-card-title class="px-6 pt-5" style="color:#1a1a2e;">
              <v-icon class="mr-2" color="#3a3a78">mdi-account-plus-outline</v-icon>
              Вступить в команду
            </v-card-title>
            <v-card-text class="px-6">
              <p class="mb-4" style="color: var(--c-text-dim);">
                Введите код команды, полученный от её лидера.
              </p>
              <v-text-field v-model="joinCode" label="Код команды" variant="outlined"
                            :error-messages="joinError" placeholder="Например: AB12CD34" />
            </v-card-text>
            <v-card-actions class="px-6 pb-6">
              <v-spacer />
              <v-btn color="#3a3a78" variant="flat"
                     :disabled="!joinCode.trim()" :loading="joining"
                     @click="joinTeam">
                Вступить
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-window-item>

      </v-window>
    </div>

    
    <v-dialog v-model="deleteDialog" max-width="340">
      <v-card class="dash-card">
        <v-card-title style="color:#1a1a2e;">Удалить команду?</v-card-title>
        <v-card-text style="color: var(--c-text-dim);">
          Команда «{{ deletingTeam?.name }}» и все её участники будут удалены безвозвратно.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="deleteDialog = false">Отмена</v-btn>
          <v-btn color="error" variant="flat" :loading="saving" @click="doDelete">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snack" color="success" timeout="3000">
      <v-icon class="mr-2">mdi-check</v-icon> {{ snackMsg }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api.js'
import { user } from '../store/auth.js'

const tab    = ref('teams')
const loading = ref(false)
const saving  = ref(false)
const teams   = ref([])
const snack   = ref(false)
const snackMsg = ref('Готово!')

const editingTeam = ref(null)
const editName    = ref('')

const switchingTeam = ref(null)
const eventCases    = ref([])
const loadingCases  = ref(false)
const selectedCase  = ref(null)
const switchingCase = ref(false)

const deleteDialog = ref(false)
const deletingTeam = ref(null)

const joinCode  = ref('')
const joinError = ref('')
const joining   = ref(false)

onMounted(async () => {
  if (!user.value) return
  await loadTeams()
})

async function loadTeams() {
  loading.value = true
  try {
    const res = await api.get(`/users/${user.value.id}/teams`)
    teams.value = res.data
  } finally {
    loading.value = false
  }
}

function toggleEdit(t) {
  if (editingTeam.value === t.id) {
    editingTeam.value = null
  } else {
    editingTeam.value = t.id
    editName.value    = t.name
    switchingTeam.value = null
  }
}

async function saveName(t) {
  saving.value = true
  try {
    await api.put(`/teams/${t.id}`, { name: editName.value, user_id: user.value.id })
    await loadTeams()
    editingTeam.value = null
    snackMsg.value = 'Название обновлено'
    snack.value = true
  } finally {
    saving.value = false
  }
}

async function toggleSwitch(t) {
  if (switchingTeam.value === t.id) {
    switchingTeam.value = null
    return
  }
  switchingTeam.value = t.id
  editingTeam.value   = null
  selectedCase.value  = null
  loadingCases.value  = true
  const res = await api.get(`/events/${t.event_slug}`)
  eventCases.value   = res.data.cases
  loadingCases.value = false
}

async function doSwitchCase(t) {
  switchingCase.value = true
  try {
    await api.put(`/teams/${t.id}`, { case_id: selectedCase.value, user_id: user.value.id })
    await loadTeams()
    switchingTeam.value = null
    snackMsg.value = 'Кейс изменён'
    snack.value = true
  } finally {
    switchingCase.value = false
  }
}

function confirmDelete(t) {
  deletingTeam.value = t
  deleteDialog.value = true
}

async function doDelete() {
  saving.value = true
  try {
    await api.delete(`/teams/${deletingTeam.value.id}`, { params: { user_id: user.value.id } })
    await loadTeams()
    deleteDialog.value = false
    snackMsg.value = 'Команда удалена'
    snack.value = true
  } finally {
    saving.value = false
  }
}

async function leaveTeam(t) {
  try {
    await api.delete(`/teams/${t.id}/leave`, { params: { user_id: user.value.id } })
    await loadTeams()
    snackMsg.value = 'Вы покинули команду'
    snack.value = true
  } catch (e) {
    snackMsg.value = e.response?.data?.detail || 'Ошибка'
    snack.value = true
  }
}

async function joinTeam() {
  joining.value   = true
  joinError.value = ''
  try {
    await api.post('/teams/join-by-code', {
      team_code: joinCode.value.trim().toUpperCase(),
      user_id: user.value.id,
    })
    await loadTeams()
    joinCode.value = ''
    tab.value = 'teams'
    snackMsg.value = 'Вы вступили в команду!'
    snack.value = true
  } catch (e) {
    joinError.value = e.response?.data?.detail || 'Неверный код команды'
  } finally {
    joining.value = false
  }
}

function copyCode(code) {
  navigator.clipboard.writeText(code)
  snackMsg.value = 'Код скопирован'
  snack.value = true
}
</script>

<style scoped>
.dash-card {
  background: var(--c-card-bg) !important;
  border: 1px solid var(--c-card-border) !important;
  border-radius: 4px !important;
  box-shadow: 2px 2px 6px rgba(0,0,0,0.10) !important;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.dash-card:hover {
  border-color: var(--c-card-border-hover) !important;
  box-shadow: 2px 2px 10px rgba(58,58,106,0.14) !important;
}
.info-item  { display: flex; flex-direction: column; margin-bottom: 16px; }
.info-label { font-size: 0.72rem; color: var(--c-text-muted); text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 3px; }
.info-val   { font-size: 0.95rem; color: #1a1a2e; }
.members-list { display: flex; flex-direction: column; gap: 5px; }
.member-row {
  display: flex; align-items: center;
  padding: 4px 8px;
  background: rgba(58,58,120,0.04);
  border-radius: 4px;
  border: 1px solid var(--c-card-border);
}
.team-code {
  font-family: monospace; font-size: 1rem;
  color: #1a5a96; letter-spacing: 2px; font-weight: 700;
  background: rgba(26,90,150,0.07); padding: 2px 8px; border-radius: 4px;
}
.expand-enter-active { transition: opacity 0.28s ease, transform 0.28s ease; }
.expand-leave-active { transition: opacity 0.18s ease; }
.expand-enter-from   { opacity: 0; transform: translateY(-8px); }
.expand-leave-to     { opacity: 0; }
</style>
