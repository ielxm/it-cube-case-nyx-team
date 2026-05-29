<template>
  <v-container class="py-8">
    <!-- Проверка авторизации -->
    <v-card v-if="!admin" class="dash-card text-center pa-10 anim-fade-up">
      <v-icon size="64" color="secondary" class="mb-4">mdi-lock-outline</v-icon>
      <h2 class="text-h6 mb-2">Доступ закрыт</h2>
      <p class="text-secondary mb-5">Только администраторы имеют доступ к этой странице</p>
      <v-btn color="secondary" variant="flat" to="/admin/login">Войти в админ-панель</v-btn>
    </v-card>

    <!-- Админ-панель -->
    <div v-else>
      <!-- Заголовок -->
      <div class="d-flex align-center justify-space-between mb-1 anim-fade-up">
        <div class="d-flex align-center">
          <v-icon color="secondary" class="mr-2">mdi-shield-admin</v-icon>
          <h1 class="text-h5 font-weight-bold">Админ-панель</h1>
        </div>
        <v-btn icon color="secondary" variant="text" @click="logout">
          <v-icon>mdi-logout</v-icon>
          <v-tooltip activator="parent">Выход</v-tooltip>
        </v-btn>
      </div>
      <p class="text-secondary mb-6 anim-fade-up delay-1">Добро пожаловать, {{ admin.name }}</p>

      <!-- Вкладки -->
      <v-tabs v-model="activeTab" color="secondary" class="mb-6 anim-fade-up delay-2">
        <v-tab value="events">Мероприятия</v-tab>
        <v-tab value="cases">Кейсы</v-tab>
        <v-tab value="limits">Лимиты</v-tab>
        <v-tab value="invites">Коды приглашения</v-tab>
        <v-tab value="stats">Статистика</v-tab>
        <v-tab value="teams">Команды</v-tab>
      </v-tabs>

      <!-- Содержимое вкладок -->
      <v-window v-model="activeTab">
        <!-- ─── МЕРОПРИЯТИЯ ─── -->
        <v-window-item value="events">
          <v-row class="mb-4">
            <v-col cols="12">
              <v-btn color="secondary" prepend-icon="mdi-plus" @click="showEventDialog = true">
                Новое мероприятие
              </v-btn>
            </v-col>
          </v-row>

          <v-row>
            <v-col v-for="event in mockEvents" :key="event.id" cols="12" md="6">
              <v-card class="dash-card">
                <v-card-title>{{ event.name }}</v-card-title>
                <v-card-text>
                  <p class="text-secondary mb-2">
                    <strong>Slug:</strong> {{ event.slug }}
                  </p>
                  <p class="text-secondary mb-2">
                    <strong>Описание:</strong> {{ event.description }}
                  </p>
                  <p class="text-secondary mb-2">
                    <strong>Кейсов:</strong> {{ event.cases.length }}
                  </p>
                  <v-chip :color="event.status === 'active' ? 'success' : 'warning'" variant="tonal" size="small">
                    {{ event.status === 'active' ? 'Активно' : 'Черновик' }}
                  </v-chip>
                </v-card-text>
                <v-card-actions>
                  <v-btn variant="text" color="secondary" @click="editEvent(event)">
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                  <v-btn variant="text" color="error" @click="deleteEventConfirm(event.id)">
                    <v-icon>mdi-trash-can</v-icon>
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
        </v-window-item>

        <!-- ─── КЕЙСЫ ─── -->
        <v-window-item value="cases">
          <v-row class="mb-4">
            <v-col cols="12">
              <v-btn color="secondary" prepend-icon="mdi-plus" @click="showCaseDialog = true">
                Новый кейс
              </v-btn>
            </v-col>
          </v-row>

          <v-data-table
            :headers="caseHeaders"
            :items="mockCases"
            class="dash-table"
          >
            <template #item.status="{ item }">
              <v-chip :color="item.status === 'active' ? 'success' : 'warning'" variant="tonal" size="small">
                {{ item.status === 'active' ? 'Активен' : 'Неактивен' }}
              </v-chip>
            </template>
            <template #item.actions="{ item }">
              <v-btn icon size="small" variant="text" @click="editCase(item)">
                <v-icon size="sm">mdi-pencil</v-icon>
              </v-btn>
              <v-btn icon size="small" variant="text" color="error" @click="deleteCaseConfirm(item.id)">
                <v-icon size="sm">mdi-trash-can</v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-window-item>

        <!-- ─── ЛИМИТЫ ─── -->
        <v-window-item value="limits">
          <v-row>
            <v-col v-for="caseItem in mockCases" :key="caseItem.id" cols="12" md="6">
              <v-card class="dash-card">
                <v-card-title class="d-flex align-center justify-space-between">
                  <span>{{ caseItem.title }}</span>
                  <v-chip size="small" :color="caseItem.occupied >= caseItem.limit ? 'error' : 'success'" variant="tonal">
                    {{ caseItem.occupied }} / {{ caseItem.limit }}
                  </v-chip>
                </v-card-title>
                <v-card-text>
                  <v-slider
                    v-model="caseItem.limit"
                    :min="1"
                    :max="20"
                    :step="1"
                    label="Лимит команд"
                    thumb-label
                    @update:model-value="updateLimit(caseItem.id, $event)"
                  />
                  <v-progress-linear
                    :value="(caseItem.occupied / caseItem.limit) * 100"
                    :color="caseItem.occupied >= caseItem.limit ? 'error' : 'success'"
                    class="mb-2"
                  />
                  <div class="text-secondary text-sm">
                    <p>Занято: {{ caseItem.occupied }}</p>
                    <p>Свободно: {{ caseItem.limit - caseItem.occupied }}</p>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-window-item>

        <!-- ─── КОДЫ ПРИГЛАШЕНИЯ ─── -->
        <v-window-item value="invites">
          <v-row class="mb-4">
            <v-col cols="12" sm="6">
              <v-select
                v-model="selectedCaseForInvite"
                :items="mockCases"
                item-title="title"
                item-value="id"
                label="Выберите кейс"
                variant="outlined"
              />
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model.number="inviteCodeCount"
                label="Количество кодов"
                type="number"
                :min="1"
                :max="100"
                variant="outlined"
              />
            </v-col>
          </v-row>

          <v-row class="mb-4">
            <v-col cols="12" sm="6">
              <v-btn color="secondary" prepend-icon="mdi-plus" block @click="generateCodes">
                Генерировать коды
              </v-btn>
            </v-col>
            <v-col cols="12" sm="6">
              <v-btn color="secondary" variant="outlined" prepend-icon="mdi-pencil" block @click="showAddCodeDialog = true">
                Добавить код вручную
              </v-btn>
            </v-col>
          </v-row>

          <v-data-table
            :headers="inviteHeaders"
            :items="mockInviteCodes"
            class="dash-table"
          >
            <template #item.used="{ item }">
              <v-chip :color="item.used ? 'error' : 'success'" variant="tonal" size="small">
                {{ item.used ? 'Использован' : 'Активен' }}
              </v-chip>
            </template>
            <template #item.code="{ item }">
              <code class="text-secondary">{{ item.code }}</code>
            </template>
            <template #item.actions="{ item }">
              <v-btn icon size="small" variant="text" @click="copyCode(item.code)">
                <v-icon size="sm">mdi-content-copy</v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-window-item>

        <!-- ─── СТАТИСТИКА ─── -->
        <v-window-item value="stats">
          <v-row class="mb-4">
            <v-col cols="12">
              <v-btn color="secondary" prepend-icon="mdi-download" @click="downloadStatsCSV">
                Загрузить статистику CSV
              </v-btn>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" md="6">
              <v-card class="dash-card">
                <v-card-title>Статистика по кейсам</v-card-title>
                <v-card-text>
                  <div v-for="stat in statsData?.cases" :key="stat.id" class="mb-4">
                    <div class="d-flex justify-space-between mb-2">
                      <strong>{{ stat.title }}</strong>
                      <span class="text-secondary text-sm">{{ stat.occupied }} / {{ stat.limit }}</span>
                    </div>
                    <v-progress-linear
                      :value="(stat.occupied / stat.limit) * 100"
                      :color="stat.occupied >= stat.limit ? 'error' : 'success'"
                    />
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" md="6">
              <v-card class="dash-card">
                <v-card-title>Общая информация</v-card-title>
                <v-card-text>
                  <v-row>
                    <v-col cols="6">
                      <div class="text-center">
                        <div class="text-h6">{{ statsData?.totalCases }}</div>
                        <p class="text-secondary text-sm">Всего кейсов</p>
                      </div>
                    </v-col>
                    <v-col cols="6">
                      <div class="text-center">
                        <div class="text-h6">{{ statsData?.totalTeams }}</div>
                        <p class="text-secondary text-sm">Зарегистрировано команд</p>
                      </div>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-window-item>

        <!-- ─── КОМАНДЫ ─── -->
        <v-window-item value="teams">
          <v-row class="mb-4">
            <v-col cols="12">
              <v-btn color="secondary" prepend-icon="mdi-download" @click="downloadTeamsCSV">
                Загрузить список команд CSV
              </v-btn>
            </v-col>
          </v-row>

          <v-data-table
            :headers="teamHeaders"
            :items="mockTeams"
            class="dash-table"
          >
            <template #item.status="{ item }">
              <v-chip :color="item.status === 'active' ? 'success' : 'warning'" variant="tonal" size="small">
                {{ item.status === 'active' ? 'Активна' : 'Неактивна' }}
              </v-chip>
            </template>
            <template #item.caseId="{ item }">
              <span>{{ getCaseName(item.caseId) }}</span>
            </template>
          </v-data-table>
        </v-window-item>
      </v-window>
    </div>

    <!-- ─── ДИАЛОГИ ─── -->

    <!-- Диалог создания/редактирования мероприятия -->
    <v-dialog v-model="showEventDialog" max-width="500">
      <v-card class="dash-card">
        <v-card-title>{{ editingEvent ? 'Редактировать мероприятие' : 'Новое мероприятие' }}</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="saveEvent">
            <v-text-field
              v-model="eventForm.name"
              label="Название"
              variant="outlined"
              class="mb-4"
              required
            />
            <v-text-field
              v-model="eventForm.slug"
              label="Slug"
              variant="outlined"
              class="mb-4"
              required
            />
            <v-textarea
              v-model="eventForm.description"
              label="Описание"
              variant="outlined"
              rows="3"
              class="mb-4"
            />
            <v-select
              v-model="eventForm.status"
              :items="['draft', 'active', 'completed']"
              label="Статус"
              variant="outlined"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="showEventDialog = false">Отмена</v-btn>
          <v-btn color="secondary" variant="flat" @click="saveEvent">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог создания/редактирования кейса -->
    <v-dialog v-model="showCaseDialog" max-width="500">
      <v-card class="dash-card">
        <v-card-title>{{ editingCase ? 'Редактировать кейс' : 'Новый кейс' }}</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="saveCase">
            <v-select
              v-model="caseForm.eventId"
              :items="mockEvents"
              item-title="name"
              item-value="id"
              label="Мероприятие"
              variant="outlined"
              class="mb-4"
              required
            />
            <v-text-field
              v-model="caseForm.title"
              label="Название кейса"
              variant="outlined"
              class="mb-4"
              required
            />
            <v-textarea
              v-model="caseForm.description"
              label="Описание"
              variant="outlined"
              rows="3"
              class="mb-4"
            />
            <v-text-field
              v-model.number="caseForm.limit"
              label="Лимит команд"
              type="number"
              :min="1"
              variant="outlined"
              class="mb-4"
              required
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="showCaseDialog = false">Отмена</v-btn>
          <v-btn color="secondary" variant="flat" @click="saveCase">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог добавления кода приглашения -->
    <v-dialog v-model="showAddCodeDialog" max-width="400">
      <v-card class="dash-card">
        <v-card-title>Добавить код приглашения</v-card-title>
        <v-card-text>
          <v-select
            v-model="addCodeForm.caseId"
            :items="mockCases"
            item-title="title"
            item-value="id"
            label="Кейс"
            variant="outlined"
            class="mb-4"
            required
          />
          <v-text-field
            v-model="addCodeForm.code"
            label="Код"
            variant="outlined"
            placeholder="ABC123"
            class="mb-4"
            required
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="showAddCodeDialog = false">Отмена</v-btn>
          <v-btn color="secondary" variant="flat" @click="saveAddCode">Добавить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="showDeleteConfirm" max-width="300">
      <v-card class="dash-card">
        <v-card-title>Подтвердить удаление</v-card-title>
        <v-card-text>Вы уверены? Это действие невозможно отменить.</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="showDeleteConfirm = false">Отмена</v-btn>
          <v-btn color="error" variant="flat" @click="confirmDelete">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  admin,
  mockEvents,
  mockCases,
  mockTeams,
  mockInviteCodes,
  logoutAdmin,
  createEvent,
  updateEvent,
  deleteEvent,
  createCase,
  updateCase,
  deleteCase,
  updateCaseLimit,
  generateInviteCode,
  addInviteCode,
  getAllStats,
  exportToCSV,
} from '../store/admin.js'

const router = useRouter()

// Проверка авторизации
if (!admin.value) {
  router.push('/admin/login')
}

// Состояние вкладок и диалогов
const activeTab = ref('events')
const showEventDialog = ref(false)
const showCaseDialog = ref(false)
const showAddCodeDialog = ref(false)
const showDeleteConfirm = ref(false)

// Формы
const eventForm = ref({ name: '', slug: '', description: '', status: 'draft' })
const caseForm = ref({ eventId: null, title: '', description: '', limit: 5 })
const addCodeForm = ref({ caseId: null, code: '' })

// Редактирование
const editingEvent = ref(null)
const editingCase = ref(null)
let deleteCallback = null

// Приглашения
const selectedCaseForInvite = ref(null)
const inviteCodeCount = ref(1)

// Таблицы
const caseHeaders = [
  { title: 'Название', key: 'title' },
  { title: 'Мероприятие', key: 'eventId' },
  { title: 'Описание', key: 'description' },
  { title: 'Лимит', key: 'limit' },
  { title: 'Занято', key: 'occupied' },
  { title: 'Статус', key: 'status' },
  { title: 'Действия', key: 'actions' },
]

const inviteHeaders = [
  { title: 'Код', key: 'code' },
  { title: 'Кейс', key: 'caseId' },
  { title: 'Статус', key: 'used' },
  { title: 'Создан', key: 'createdAt' },
  { title: 'Действия', key: 'actions' },
]

const teamHeaders = [
  { title: 'Название', key: 'name' },
  { title: 'Капитан', key: 'captain' },
  { title: 'Email', key: 'email' },
  { title: 'Телефон', key: 'phone' },
  { title: 'Кейс', key: 'caseId' },
  { title: 'Статус', key: 'status' },
]

const statsData = computed(() => {
  if (mockEvents.value.length > 0) {
    return getAllStats(mockEvents.value[0].id)
  }
  return null
})

// Методы
function logout() {
  logoutAdmin()
  router.push('/admin/login')
}

function editEvent(event) {
  editingEvent.value = event
  eventForm.value = {
    name: event.name,
    slug: event.slug,
    description: event.description,
    status: event.status,
  }
  showEventDialog.value = true
}

function saveEvent() {
  if (editingEvent.value) {
    updateEvent(editingEvent.value.id, eventForm.value)
    editingEvent.value = null
  } else {
    createEvent(eventForm.value)
  }
  eventForm.value = { name: '', slug: '', description: '', status: 'draft' }
  showEventDialog.value = false
}

function deleteEventConfirm(eventId) {
  deleteCallback = () => deleteEvent(eventId)
  showDeleteConfirm.value = true
}

function editCase(caseItem) {
  editingCase.value = caseItem
  caseForm.value = {
    eventId: caseItem.eventId,
    title: caseItem.title,
    description: caseItem.description,
    limit: caseItem.limit,
  }
  showCaseDialog.value = true
}

function saveCase() {
  if (editingCase.value) {
    updateCase(editingCase.value.id, caseForm.value)
    editingCase.value = null
  } else {
    createCase(caseForm.value)
  }
  caseForm.value = { eventId: null, title: '', description: '', limit: 5 }
  showCaseDialog.value = false
}

function deleteCaseConfirm(caseId) {
  deleteCallback = () => deleteCase(caseId)
  showDeleteConfirm.value = true
}

function confirmDelete() {
  if (deleteCallback) {
    deleteCallback()
    deleteCallback = null
  }
  showDeleteConfirm.value = false
}

function updateLimit(caseId, newLimit) {
  updateCaseLimit(caseId, newLimit)
}

function generateCodes() {
  if (selectedCaseForInvite.value) {
    generateInviteCode(selectedCaseForInvite.value, inviteCodeCount.value)
    selectedCaseForInvite.value = null
    inviteCodeCount.value = 1
  }
}

function saveAddCode() {
  if (addCodeForm.value.caseId && addCodeForm.value.code) {
    addInviteCode(addCodeForm.value.code, addCodeForm.value.caseId)
    addCodeForm.value = { caseId: null, code: '' }
    showAddCodeDialog.value = false
  }
}

function copyCode(code) {
  navigator.clipboard.writeText(code)
  alert('Код скопирован: ' + code)
}

function getCaseName(caseId) {
  return mockCases.value.find(c => c.id === caseId)?.title || 'Неизвестно'
}

function downloadStatsCSV() {
  if (statsData.value) {
    exportToCSV(statsData.value, 'stats.csv')
  }
}

function downloadTeamsCSV() {
  exportToCSV(mockTeams.value, 'teams.csv')
}
</script>

<style scoped>
.dash-card {
  border: 1px solid var(--c-card-border);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.dash-card:hover {
  border-color: var(--c-card-border-hover);
  box-shadow: 0 0 20px var(--c-card-glow);
}

.dash-table {
  background: transparent;
}

.anim-fade-up {
  animation: fadeUp 0.6s ease-out forwards;
  opacity: 0;
}

.delay-1 {
  animation-delay: 0.1s;
}

.delay-2 {
  animation-delay: 0.2s;
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
