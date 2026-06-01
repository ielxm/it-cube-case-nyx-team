<template>
  <div class="admin-dash-page">

    
    <div v-if="!admin" class="form-wrap">
      <v-card class="dash-card text-center pa-10" :elevation="0" max-width="420">
        <v-icon size="56" color="secondary" class="mb-4">mdi-lock-outline</v-icon>
        <h2 class="card-title mb-2">Доступ закрыт</h2>
        <p class="card-sub mb-5">Только администраторы имеют доступ к этой странице</p>
        <v-btn color="secondary" variant="flat" rounded="sm" to="/admin/login">
          Войти в панель
        </v-btn>
      </v-card>
    </div>

    
    <div v-else>

      
      <section class="dash-hero">
        <div class="dash-hero-inner">
          <div class="dash-hero-brand">
            <v-icon color="#b8b8d0" size="26" class="mr-2">mdi-shield-admin</v-icon>
            <span class="dash-hero-title">Панель администратора</span>
          </div>
          <div class="dash-hero-right">
            <span class="dash-hero-user">{{ admin.name || admin.email }}</span>
            <v-btn icon variant="text" size="small" class="dash-hero-logout" @click="logout">
              <v-icon size="18">mdi-logout</v-icon>
              <v-tooltip activator="parent" location="bottom">Выйти</v-tooltip>
            </v-btn>
          </div>
        </div>
      </section>

      <v-container class="py-5">
        <v-progress-linear v-if="globalLoading" indeterminate color="secondary" class="mb-4" />

        <v-tabs v-model="activeTab" color="secondary" class="mb-5 dash-tabs">
          <v-tab value="events">Мероприятия</v-tab>
          <v-tab value="cases">Кейсы</v-tab>
          <v-tab value="limits">Лимиты</v-tab>
          <v-tab value="invites">Приглашения</v-tab>
          <v-tab value="stats">Статистика</v-tab>
          <v-tab value="teams">Команды</v-tab>
          <v-tab value="admins">Администраторы</v-tab>
        </v-tabs>

        <v-window v-model="activeTab">

          
          <v-window-item value="events">
            <v-row class="mb-4">
              <v-col>
                <v-btn color="secondary" variant="flat" rounded="sm" prepend-icon="mdi-plus" @click="openEventDialog()">
                  Новое мероприятие
                </v-btn>
              </v-col>
            </v-row>
            <v-row>
              <v-col v-for="ev in mockEvents" :key="ev.id" cols="12" md="6">
                <v-card class="dash-card" :elevation="0">
                  <v-card-title class="card-section-title pt-4 px-4">{{ ev.title }}</v-card-title>
                  <v-card-text class="px-4">
                    <p class="card-meta mb-1"><strong>Slug:</strong> {{ ev.slug }}</p>
                    <p class="card-meta mb-1"><strong>Место:</strong> {{ ev.location }}</p>
                    <p class="card-meta mb-3"><strong>Кейсов:</strong> {{ ev.cases_count }}</p>
                    <v-chip :color="ev.is_active ? 'success' : 'warning'" variant="tonal" size="small">
                      {{ ev.is_active ? 'Активно' : 'Неактивно' }}
                    </v-chip>
                  </v-card-text>
                  <v-card-actions class="px-4 pb-4">
                    <v-btn variant="text" color="secondary" size="small" @click="openEventDialog(ev)">
                      <v-icon size="18">mdi-pencil</v-icon>
                    </v-btn>
                    <v-btn variant="text" color="error" size="small" @click="deleteEventConfirm(ev.id)">
                      <v-icon size="18">mdi-trash-can</v-icon>
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
          </v-window-item>

          
          <v-window-item value="cases">
            <v-row class="mb-4">
              <v-col>
                <v-btn color="secondary" variant="flat" rounded="sm" prepend-icon="mdi-plus" @click="openCaseDialog()">
                  Новый кейс
                </v-btn>
              </v-col>
            </v-row>
            <v-card class="dash-card" :elevation="0">
              <v-data-table :headers="caseHeaders" :items="mockCases" class="dash-table">
                <template #item.actions="{ item }">
                  <v-btn icon size="small" variant="text" @click="openCaseDialog(item)">
                    <v-icon size="16">mdi-pencil</v-icon>
                  </v-btn>
                  <v-btn icon size="small" variant="text" color="error" @click="deleteCaseConfirm(item.id)">
                    <v-icon size="16">mdi-trash-can</v-icon>
                  </v-btn>
                </template>
              </v-data-table>
            </v-card>
          </v-window-item>

          
          <v-window-item value="limits">
            <v-row>
              <v-col v-for="c in mockCases" :key="c.id" cols="12" md="6">
                <v-card class="dash-card" :elevation="0">
                  <v-card-title class="d-flex align-center justify-space-between pt-4 px-4 card-section-title">
                    <span>{{ c.title }}</span>
                    <v-chip size="small" :color="c.registered >= c.limit_teams ? 'error' : 'success'" variant="tonal">
                      {{ c.registered }} / {{ c.limit_teams }}
                    </v-chip>
                  </v-card-title>
                  <v-card-text class="px-4 pb-4">
                    <v-slider v-model="c.limit_teams" :min="1" :max="20" :step="1"
                      label="Лимит команд" thumb-label color="secondary"
                      @end="saveLimit(c)" />
                    <div class="card-meta">
                      <p>Занято: {{ c.registered }}</p>
                      <p>Свободно: {{ c.limit_teams - c.registered }}</p>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-window-item>

          
          <v-window-item value="invites">
            <v-row class="mb-4">
              <v-col cols="12" sm="6">
                <v-select v-model="selectedEventForInvite" :items="mockEvents"
                  item-title="title" item-value="id"
                  label="Мероприятие" variant="outlined" density="comfortable"
                  @update:model-value="loadCodes" />
              </v-col>
              <v-col cols="12" sm="3">
                <v-text-field v-model.number="inviteCodeCount" label="Количество"
                  type="number" :min="1" :max="100" variant="outlined" density="comfortable" />
              </v-col>
              <v-col cols="12" sm="3" class="d-flex align-center gap-2">
                <v-btn color="secondary" variant="flat" rounded="sm" prepend-icon="mdi-plus"
                  :disabled="!selectedEventForInvite" :loading="generatingCodes"
                  @click="generateCodes">
                  Генерировать
                </v-btn>
                <v-btn color="secondary" variant="outlined" rounded="sm" prepend-icon="mdi-pencil"
                  :disabled="!selectedEventForInvite"
                  @click="showAddCodeDialog = true">
                  Вручную
                </v-btn>
              </v-col>
            </v-row>
            <v-progress-linear v-if="loadingCodes" indeterminate color="secondary" class="mb-3" />
            <v-card class="dash-card" :elevation="0">
              <v-data-table :headers="inviteHeaders" :items="mockInviteCodes" class="dash-table">
                <template #item.is_used="{ item }">
                  <v-chip :color="item.is_used ? 'error' : 'success'" variant="tonal" size="small">
                    {{ item.is_used ? 'Использован' : 'Активен' }}
                  </v-chip>
                </template>
                <template #item.code="{ item }">
                  <code class="invite-code">{{ item.code }}</code>
                </template>
                <template #item.actions="{ item }">
                  <v-btn icon size="small" variant="text" @click="copyCode(item.code)">
                    <v-icon size="16">mdi-content-copy</v-icon>
                  </v-btn>
                </template>
              </v-data-table>
            </v-card>
          </v-window-item>

          
          <v-window-item value="stats">
            <v-row class="mb-4">
              <v-col>
                <v-btn color="secondary" variant="flat" rounded="sm" prepend-icon="mdi-download"
                  @click="downloadStatsCSV">
                  Скачать CSV
                </v-btn>
              </v-col>
            </v-row>
            <v-row v-if="statsData">
              <v-col cols="12" md="6">
                <v-card class="dash-card" :elevation="0">
                  <v-card-title class="card-section-title pt-4 px-4">Статистика по кейсам</v-card-title>
                  <v-divider />
                  <v-card-text class="pa-4">
                    <div v-for="c in statsData.cases" :key="c.id" class="mb-4">
                      <div class="d-flex justify-space-between mb-1">
                        <span class="stats-case-title">{{ c.title }}</span>
                        <span class="card-meta">{{ c.registered }} / {{ c.limit_teams }}</span>
                      </div>
                      <v-progress-linear
                        :model-value="(c.registered / c.limit_teams) * 100"
                        :color="c.registered >= c.limit_teams ? 'error' : 'success'"
                        bg-color="rgba(128,128,128,0.1)" rounded height="6" />
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card class="dash-card" :elevation="0">
                  <v-card-title class="card-section-title pt-4 px-4">Общая информация</v-card-title>
                  <v-divider />
                  <v-card-text class="pa-4">
                    <v-row>
                      <v-col cols="4" class="text-center">
                        <div class="stats-num">{{ statsData.totalCases }}</div>
                        <p class="card-meta">Кейсов</p>
                      </v-col>
                      <v-col cols="4" class="text-center">
                        <div class="stats-num">{{ statsData.totalTeams }}</div>
                        <p class="card-meta">Команд</p>
                      </v-col>
                      <v-col cols="4" class="text-center">
                        <div class="stats-num">{{ statsData.totalMembers }}</div>
                        <p class="card-meta">Участников</p>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
            <div v-else class="text-center py-8">
              <v-progress-circular indeterminate color="secondary" size="36" />
            </div>
          </v-window-item>

          
          <v-window-item value="teams">
            <v-row class="mb-4">
              <v-col>
                <v-btn color="secondary" variant="flat" rounded="sm" prepend-icon="mdi-download"
                  @click="downloadTeamsCSV">
                  Скачать CSV
                </v-btn>
              </v-col>
            </v-row>
            <v-card class="dash-card" :elevation="0">
              <v-data-table :headers="teamHeaders" :items="mockTeams" class="dash-table" />
            </v-card>
          </v-window-item>

          
          <v-window-item value="admins">
            <v-row>

              
              <v-col cols="12" md="7">
                <v-card class="dash-card" :elevation="0">
                  <v-card-title class="card-section-title pt-4 px-4">Список администраторов</v-card-title>
                  <v-divider />
                  <v-card-text class="pa-3">
                    <div v-if="adminLoadingList" class="text-center py-6">
                      <v-progress-circular indeterminate color="secondary" size="28" />
                    </div>
                    <div v-else class="admins-list">
                      <div v-for="a in adminsList" :key="a.id" class="admin-row">
                        <div class="admin-row-info">
                          <v-icon size="16" color="secondary" class="mr-2">mdi-account-circle</v-icon>
                          <div>
                            <div class="admin-name">{{ a.name }}</div>
                            <div class="admin-email">{{ a.email }}</div>
                          </div>
                        </div>
                        <div class="admin-row-actions">
                          <span class="admin-date">{{ a.created_at?.slice(0, 10) }}</span>
                          <v-btn
                            icon size="x-small" variant="text" color="error"
                            :disabled="a.id === admin?.admin_id"
                            @click="confirmDeleteAdmin(a)"
                          >
                            <v-icon size="15">mdi-trash-can</v-icon>
                            <v-tooltip activator="parent" location="left">Удалить</v-tooltip>
                          </v-btn>
                        </div>
                      </div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>

              
              <v-col cols="12" md="5">
                <v-card class="dash-card" :elevation="0">
                  <v-card-title class="card-section-title pt-4 px-4">Создать администратора</v-card-title>
                  <v-divider />
                  <v-card-text class="pa-4">
                    <v-text-field
                      v-model="newAdmin.name"
                      label="Имя"
                      variant="outlined"
                      density="comfortable"
                      prepend-inner-icon="mdi-account"
                      class="mb-3"
                    />
                    <v-text-field
                      v-model="newAdmin.email"
                      label="Email"
                      type="email"
                      variant="outlined"
                      density="comfortable"
                      prepend-inner-icon="mdi-email-outline"
                      class="mb-3"
                    />
                    <v-text-field
                      v-model="newAdmin.password"
                      label="Пароль (мин. 6 символов)"
                      type="password"
                      variant="outlined"
                      density="comfortable"
                      prepend-inner-icon="mdi-lock-outline"
                      class="mb-4"
                    />
                    <v-alert v-if="adminCreateError" type="error" variant="tonal" density="compact" class="mb-3">
                      {{ adminCreateError }}
                    </v-alert>
                    <v-btn
                      color="secondary" variant="flat" rounded="sm" block
                      :loading="adminCreating"
                      @click="doCreateAdmin"
                    >
                      Создать администратора
                    </v-btn>
                  </v-card-text>
                </v-card>
              </v-col>

            </v-row>
          </v-window-item>

        </v-window>
      </v-container>
    </div>

    

    <v-dialog v-model="showEventDialog" max-width="500">
      <v-card class="dash-card" :elevation="0">
        <v-card-title class="card-section-title pt-4 px-4">
          {{ editingEvent ? 'Редактировать мероприятие' : 'Новое мероприятие' }}
        </v-card-title>
        <v-divider />
        <v-card-text class="pa-4">
          <v-text-field v-model="eventForm.title"       label="Название"  variant="outlined" density="comfortable" class="mb-3" />
          <v-text-field v-model="eventForm.slug"        label="Slug"      variant="outlined" density="comfortable" class="mb-3" />
          <v-text-field v-model="eventForm.location"    label="Место"     variant="outlined" density="comfortable" class="mb-3" />
          <v-textarea   v-model="eventForm.description" label="Описание"  variant="outlined" rows="3"              class="mb-3" />
          <v-select v-model="eventForm.is_active"
            :items="[{title:'Активно',value:1},{title:'Неактивно',value:0}]"
            item-title="title" item-value="value"
            label="Статус" variant="outlined" density="comfortable" />
        </v-card-text>
        <v-card-actions class="px-4 pb-4">
          <v-spacer />
          <v-btn variant="text" @click="showEventDialog = false">Отмена</v-btn>
          <v-btn color="secondary" variant="flat" rounded="sm" :loading="saving" @click="saveEvent">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showCaseDialog" max-width="500">
      <v-card class="dash-card" :elevation="0">
        <v-card-title class="card-section-title pt-4 px-4">
          {{ editingCase ? 'Редактировать кейс' : 'Новый кейс' }}
        </v-card-title>
        <v-divider />
        <v-card-text class="pa-4">
          <v-select v-model="caseForm.event_id" :items="mockEvents"
            item-title="title" item-value="id"
            label="Мероприятие" variant="outlined" density="comfortable" class="mb-3" />
          <v-text-field v-model="caseForm.title"             label="Название"     variant="outlined" density="comfortable" class="mb-3" />
          <v-textarea   v-model="caseForm.description"       label="Описание"     variant="outlined" rows="3"              class="mb-3" />
          <v-text-field v-model.number="caseForm.limit_teams" label="Лимит команд" type="number" :min="1"
            variant="outlined" density="comfortable" />
        </v-card-text>
        <v-card-actions class="px-4 pb-4">
          <v-spacer />
          <v-btn variant="text" @click="showCaseDialog = false">Отмена</v-btn>
          <v-btn color="secondary" variant="flat" rounded="sm" :loading="saving" @click="saveCase">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showAddCodeDialog" max-width="400">
      <v-card class="dash-card" :elevation="0">
        <v-card-title class="card-section-title pt-4 px-4">Добавить код приглашения</v-card-title>
        <v-divider />
        <v-card-text class="pa-4">
          <v-select v-model="addCodeForm.eventId" :items="mockEvents"
            item-title="title" item-value="id"
            label="Мероприятие" variant="outlined" density="comfortable" class="mb-3" />
          <v-text-field v-model="addCodeForm.code" label="Код" variant="outlined" density="comfortable"
            placeholder="ABC123" class="mb-3" />
          <v-alert v-if="addCodeError" type="error" variant="tonal" density="compact">{{ addCodeError }}</v-alert>
        </v-card-text>
        <v-card-actions class="px-4 pb-4">
          <v-spacer />
          <v-btn variant="text" @click="showAddCodeDialog = false; addCodeError = ''">Отмена</v-btn>
          <v-btn color="secondary" variant="flat" rounded="sm" :loading="savingCode" @click="saveAddCode">Добавить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showDeleteConfirm" max-width="340">
      <v-card class="dash-card" :elevation="0">
        <v-card-title class="card-section-title pt-4 px-4">Подтвердить удаление</v-card-title>
        <v-divider />
        <v-card-text class="pa-4">Вы уверены? Это действие невозможно отменить.</v-card-text>
        <v-card-actions class="px-4 pb-4">
          <v-spacer />
          <v-btn variant="text" @click="showDeleteConfirm = false">Отмена</v-btn>
          <v-btn color="error" variant="flat" rounded="sm" :loading="saving" @click="confirmDelete">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snack" color="success" timeout="2500">{{ snackMsg }}</v-snackbar>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  admin, mockEvents, mockCases, mockTeams, mockInviteCodes, adminsList,
  logoutAdmin, fetchAll, fetchTeams,
  fetchInviteCodes, generateInviteCode, addInviteCode,
  createEvent, updateEvent, deleteEvent,
  createCase, updateCase, deleteCase,
  fetchAdminStats, exportToCSV,
  fetchAdminsList, createAdminAccount, deleteAdminAccount,
} from '../store/admin.js'

const router = useRouter()
if (!admin.value) router.push('/admin/login')

const activeTab      = ref('events')
const globalLoading  = ref(false)
const saving         = ref(false)
const snack          = ref(false)
const snackMsg       = ref('Готово!')

const showEventDialog   = ref(false)
const showCaseDialog    = ref(false)
const showAddCodeDialog = ref(false)
const showDeleteConfirm = ref(false)

const eventForm   = ref({ title: '', slug: '', description: '', location: 'IT Cube', is_active: 1 })
const caseForm    = ref({ event_id: null, title: '', description: '', limit_teams: 8 })
const addCodeForm = ref({ eventId: null, code: '' })

const editingEvent = ref(null)
const editingCase  = ref(null)
let   deleteCallback = null

const selectedEventForInvite = ref(null)
const inviteCodeCount  = ref(1)
const loadingCodes     = ref(false)
const generatingCodes  = ref(false)
const addCodeError     = ref('')
const savingCode       = ref(false)
const statsData        = ref(null)

const adminLoadingList = ref(false)
const adminCreating    = ref(false)
const adminCreateError = ref('')
const newAdmin         = ref({ name: '', email: '', password: '' })

const caseHeaders = [
  { title: 'Название',         key: 'title'       },
  { title: 'Мероприятие',      key: 'event_title' },
  { title: 'Лимит',            key: 'limit_teams' },
  { title: 'Зарегистрировано', key: 'registered'  },
  { title: 'Действия',         key: 'actions'     },
]
const inviteHeaders = [
  { title: 'Код',         key: 'code'        },
  { title: 'Мероприятие', key: 'event_title' },
  { title: 'Статус',      key: 'is_used'     },
  { title: '',            key: 'actions'     },
]
const teamHeaders = [
  { title: 'Команда',     key: 'name'         },
  { title: 'Лидер',       key: 'leader_name'  },
  { title: 'Мероприятие', key: 'event_title'  },
  { title: 'Кейс',        key: 'case_title'   },
  { title: 'Участников',  key: 'member_count' },
  { title: 'Код команды', key: 'team_code'    },
]

onMounted(async () => {
  globalLoading.value = true
  await fetchAll()
  globalLoading.value = false
})

watch(activeTab, async val => {
  if (val === 'invites') loadCodes()
  if (val === 'teams')   fetchTeams()
  if (val === 'stats')   loadStats()
  if (val === 'admins')  loadAdmins()
})

async function loadCodes() {
  loadingCodes.value = true
  await fetchInviteCodes(selectedEventForInvite.value || null)
  loadingCodes.value = false
}

async function loadStats() {
  statsData.value = null
  statsData.value = await fetchAdminStats()
}

async function loadAdmins() {
  adminLoadingList.value = true
  await fetchAdminsList()
  adminLoadingList.value = false
}

function logout() { logoutAdmin(); router.push('/admin/login') }

function openEventDialog(ev = null) {
  editingEvent.value = ev
  eventForm.value = ev
    ? { title: ev.title, slug: ev.slug, description: ev.description, location: ev.location, is_active: ev.is_active }
    : { title: '', slug: '', description: '', location: 'IT Cube', is_active: 1 }
  showEventDialog.value = true
}

async function saveEvent() {
  saving.value = true
  try {
    if (editingEvent.value) await updateEvent(editingEvent.value.id, eventForm.value)
    else                    await createEvent(eventForm.value)
    showEventDialog.value = false
    showSnack('Мероприятие сохранено')
  } finally { saving.value = false }
}

function deleteEventConfirm(id) {
  deleteCallback = () => deleteEvent(id)
  showDeleteConfirm.value = true
}

function openCaseDialog(c = null) {
  editingCase.value = c
  caseForm.value = c
    ? { event_id: c.event_id, title: c.title, description: c.description, limit_teams: c.limit_teams }
    : { event_id: null, title: '', description: '', limit_teams: 8 }
  showCaseDialog.value = true
}

async function saveCase() {
  saving.value = true
  try {
    if (editingCase.value) await updateCase(editingCase.value.id, caseForm.value)
    else                   await createCase(caseForm.value)
    showCaseDialog.value = false
    showSnack('Кейс сохранён')
  } finally { saving.value = false }
}

function deleteCaseConfirm(id) {
  deleteCallback = () => deleteCase(id)
  showDeleteConfirm.value = true
}

async function confirmDelete() {
  if (!deleteCallback) return
  saving.value = true
  try { await deleteCallback(); showSnack('Удалено') }
  finally { saving.value = false; deleteCallback = null; showDeleteConfirm.value = false }
}

async function saveLimit(caseItem) {
  await updateCase(caseItem.id, {
    event_id: caseItem.event_id,
    title: caseItem.title,
    description: caseItem.description,
    limit_teams: caseItem.limit_teams,
  })
  showSnack('Лимит обновлён')
}

async function generateCodes() {
  if (!selectedEventForInvite.value) return
  generatingCodes.value = true
  await generateInviteCode(selectedEventForInvite.value, inviteCodeCount.value)
  inviteCodeCount.value = 1
  generatingCodes.value = false
  showSnack('Коды сгенерированы')
}

async function saveAddCode() {
  if (!addCodeForm.value.eventId || !addCodeForm.value.code) return
  savingCode.value  = true
  addCodeError.value = ''
  try {
    await addInviteCode(addCodeForm.value.code, addCodeForm.value.eventId)
    addCodeForm.value = { eventId: null, code: '' }
    showAddCodeDialog.value = false
    showSnack('Код добавлен')
  } catch (e) {
    addCodeError.value = e.message
  } finally { savingCode.value = false }
}

function copyCode(code) {
  navigator.clipboard.writeText(code)
  showSnack('Код скопирован')
}

function downloadStatsCSV() {
  if (statsData.value) exportToCSV(statsData.value, 'stats.csv')
}

function downloadTeamsCSV() {
  exportToCSV(mockTeams.value, 'teams.csv')
}

async function doCreateAdmin() {
  adminCreateError.value = ''
  if (!newAdmin.value.name || !newAdmin.value.email || !newAdmin.value.password) {
    adminCreateError.value = 'Заполните все поля'
    return
  }
  adminCreating.value = true
  try {
    await createAdminAccount(newAdmin.value)
    newAdmin.value = { name: '', email: '', password: '' }
    showSnack('Администратор создан')
  } catch (e) {
    adminCreateError.value = e.response?.data?.detail || 'Ошибка при создании'
  } finally { adminCreating.value = false }
}

async function confirmDeleteAdmin(a) {
  if (!confirm(`Удалить администратора ${a.email}?`)) return
  try {
    await deleteAdminAccount(a.id)
    showSnack('Администратор удалён')
  } catch (e) {
    showSnack(e.response?.data?.detail || 'Ошибка при удалении')
  }
}

function showSnack(msg) {
  snackMsg.value = msg
  snack.value    = true
}
</script>

<style scoped>
.admin-dash-page {
  min-height: 100vh;
  background: var(--c-page-bg);
  font-family: Arial, Helvetica, sans-serif;
}

/* Not-auth centering */
.form-wrap {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px 16px;
}

/* Hero header */
.dash-hero {
  background: linear-gradient(180deg, #2e2e42 0%, #1e1e2e 100%);
  border-bottom: 2px solid #111120;
  padding: 14px 0;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.40);
}

.dash-hero-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.dash-hero-brand {
  display: flex;
  align-items: center;
}

.dash-hero-title {
  font-family: 'PT Serif', Georgia, serif;
  font-size: 17px;
  font-weight: 700;
  color: #e8e8f4;
  letter-spacing: 1px;
}

.dash-hero-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.dash-hero-user {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 12px;
  color: #8888b8;
}

.dash-hero-logout {
  color: #7878a0 !important;
}

/* Tabs */
.dash-tabs {
  border-bottom: 1px solid var(--c-card-border);
}

/* Cards — same as home-card / case-card */
.dash-card {
  background: var(--c-card-bg) !important;
  border: 1px solid var(--c-card-border) !important;
  border-radius: 4px !important;
  transition: border-color 0.25s, box-shadow 0.25s;
  margin-bottom: 12px;
}

.dash-card:hover {
  border-color: var(--c-card-border-hover) !important;
  box-shadow: 0 0 24px var(--c-card-glow) !important;
}

.dash-table { background: transparent !important; }

.card-section-title {
  font-family: 'PT Serif', Georgia, Times, serif;
  font-size: 14px !important;
  font-weight: 700 !important;
  color: #1a1a28;
}

.card-meta {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 12px;
  color: var(--c-text-dim);
}

/* Stats */
.stats-num {
  font-family: 'PT Serif', Georgia, serif;
  font-size: 26px;
  font-weight: 700;
  color: #1a1a6a;
}

.stats-case-title {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 12px;
  font-weight: 600;
  color: #1a1a28;
  max-width: 70%;
}

/* Invite code */
.invite-code {
  font-family: 'Courier New', monospace;
  font-size: 13px;
  background: rgba(58, 58, 106, 0.07);
  padding: 2px 6px;
  border-radius: 3px;
  color: #1a1a6a;
}

/* Admins list */
.admins-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.admin-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 9px 8px;
  border-bottom: 1px solid var(--c-card-border);
}

.admin-row:last-child { border-bottom: none; }

.admin-row-info {
  display: flex;
  align-items: center;
}

.admin-name {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 13px;
  font-weight: 600;
  color: #1a1a28;
}

.admin-email {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 11px;
  color: var(--c-text-dim);
}

.admin-row-actions {
  display: flex;
  align-items: center;
  gap: 6px;
}

.admin-date {
  font-size: 11px;
  color: var(--c-text-muted);
}
</style>
