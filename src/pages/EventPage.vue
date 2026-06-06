<template>
  <v-container class="py-8">
    <div v-if="loading" class="text-center py-16">
      <v-progress-circular indeterminate color="secondary" size="48" />
    </div>
    <div v-else-if="notFound" class="anim-fade-in">
      <h2 class="text-h5 font-weight-bold mb-6">Мероприятия</h2>

      <template v-if="loadingAll">
        <div class="text-center py-10">
          <v-progress-circular indeterminate color="secondary" size="36" />
        </div>
      </template>
      <template v-else>

        <!-- Запланированные -->
        <div class="mb-8">
          <p class="section-label mb-3">Запланированные</p>
          <div v-if="plannedEvents.length" class="events-list">
            <div v-for="ev in plannedEvents" :key="ev.id"
                 class="event-row" @click="$router.push('/events/' + ev.slug)">
              <div class="event-header">
                <v-icon size="14" color="success" class="mr-1">mdi-calendar-clock</v-icon>
                <span class="event-title">{{ ev.title }}</span>
                <v-chip color="success" variant="tonal" size="x-small" class="ml-2">РЕГИСТРАЦИЯ</v-chip>
              </div>
              <p class="event-desc">{{ ev.description }}</p>
              <div class="event-footer">
                <span class="event-meta">
                  <v-icon size="11">mdi-briefcase-outline</v-icon>
                  {{ ev.cases_count || 0 }}&nbsp;кейсов
                </span>
                <span class="event-meta">
                  <v-icon size="11">mdi-map-marker-outline</v-icon>
                  {{ ev.location || '—' }}
                </span>
                <span v-if="ev.start_date" class="event-meta event-meta--date">
                  <v-icon size="11">mdi-calendar-arrow-right</v-icon>
                  Начало: {{ formatDate(ev.start_date) }}
                </span>
                <a class="event-more" @click.stop="$router.push('/events/' + ev.slug)">Подробнее&nbsp;→</a>
              </div>
            </div>
          </div>
          <p v-else class="empty-msg">Запланированных мероприятий пока нет</p>
        </div>

        <!-- Активные -->
        <div class="mb-8">
          <p class="section-label mb-3">Активные</p>
          <div v-if="activeEvents.length" class="events-list">
            <div v-for="ev in activeEvents" :key="ev.id"
                 class="event-row event-row--active" @click="$router.push('/events/' + ev.slug)">
              <div class="event-header">
                <v-icon size="14" color="primary" class="mr-1">mdi-calendar-star</v-icon>
                <span class="event-title">{{ ev.title }}</span>
                <v-chip color="primary" variant="tonal" size="x-small" class="ml-2">ИДЁТ</v-chip>
              </div>
              <p class="event-desc">{{ ev.description }}</p>
              <div class="event-footer">
                <span class="event-meta">
                  <v-icon size="11">mdi-briefcase-outline</v-icon>
                  {{ ev.cases_count || 0 }}&nbsp;кейсов
                </span>
                <span class="event-meta">
                  <v-icon size="11">mdi-map-marker-outline</v-icon>
                  {{ ev.location || '—' }}
                </span>
                <a class="event-more" @click.stop="$router.push('/events/' + ev.slug)">Подробнее&nbsp;→</a>
              </div>
            </div>
          </div>
          <p v-else class="empty-msg">Активных мероприятий нет</p>
        </div>

        <!-- Завершённые -->
        <div v-if="inactiveEvents.length">
          <p class="section-label mb-3">Завершённые</p>
          <div class="events-list">
            <div v-for="ev in inactiveEvents" :key="ev.id"
                 class="event-row event-row--inactive" @click="$router.push('/events/' + ev.slug)">
              <div class="event-header">
                <v-icon size="14" color="grey" class="mr-1">mdi-calendar-check</v-icon>
                <span class="event-title event-title--inactive">{{ ev.title }}</span>
                <v-chip color="grey" variant="tonal" size="x-small" class="ml-2">ЗАВЕРШЕНО</v-chip>
              </div>
              <p class="event-desc">{{ ev.description }}</p>
              <div class="event-footer">
                <span class="event-meta">
                  <v-icon size="11">mdi-briefcase-outline</v-icon>
                  {{ ev.cases_count || 0 }}&nbsp;кейсов
                </span>
                <span class="event-meta">
                  <v-icon size="11">mdi-map-marker-outline</v-icon>
                  {{ ev.location || '—' }}
                </span>
                <a class="event-more" @click.stop="$router.push('/events/' + ev.slug)">Подробнее&nbsp;→</a>
              </div>
            </div>
          </div>
        </div>

      </template>
    </div>
    <div v-else>
      <v-btn variant="text" prepend-icon="mdi-arrow-left" to="/" class="mb-6 anim-fade-in" color="secondary">
        Все мероприятия
      </v-btn>
      <div class="mb-8 anim-fade-up">
        <h1 class="text-h4 font-weight-bold">{{ event.title }}</h1>
        <p class="mt-2 mb-3" style="max-width: 680px; line-height: 1.6; color: var(--c-text-dim);">{{ event.description }}</p>
        <div class="d-flex align-center gap-3 flex-wrap">
          <v-chip :color="statusColor(event.status)" variant="tonal">{{ statusLabel(event.status) }}</v-chip>
          <span v-if="event.status === 'planned' && event.start_date" class="start-date-hint">
            <v-icon size="14" class="mr-1">mdi-calendar-clock</v-icon>Начало: {{ formatDate(event.start_date) }}
          </span>
        </div>
      </div>
      <h2 class="text-h5 font-weight-bold mb-4 anim-fade-up delay-1">Доступные кейсы</h2>
      <v-row>
        <v-col v-for="(c, i) in event.cases" :key="c.id" cols="12" md="6"
               :class="`anim-fade-up delay-${i + 2}`">
          <v-card class="case-card d-flex flex-column">
            <v-card-title class="pt-5 px-5">{{ c.title }}</v-card-title>
            <v-card-text class="px-5 flex-grow-1">
              <p class="mb-4" style="line-height: 1.6; color: var(--c-text-dim);">{{ c.description }}</p>
              <v-progress-linear :model-value="(c.registered / c.limit_teams) * 100"
                                 color="secondary" bg-color="rgba(128,128,128,0.1)"
                                 rounded height="6" class="mb-1" />
              <span class="spots-text">{{ c.registered }} / {{ c.limit_teams }} команд зарегистрировано</span>
            </v-card-text>
            <v-card-actions class="px-5 pb-5">
              <v-chip v-if="event.status === 'planned'"
                      :color="c.registered < c.limit_teams ? 'success' : 'error'" variant="tonal" size="small">
                {{ c.registered < c.limit_teams ? `Свободно ${c.limit_teams - c.registered} мест` : 'Мест нет' }}
              </v-chip>
              <v-chip v-else color="grey" variant="tonal" size="small">Регистрация закрыта</v-chip>
              <v-spacer />
              <v-btn v-if="event.status === 'planned'" color="secondary" variant="flat" size="small"
                     :disabled="c.registered >= c.limit_teams" @click="goRegister(c.id)">
                Зарегистрироваться
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api.js'
import { user } from '../store/auth.js'

const route = useRoute(), router = useRouter()
const event = ref({ cases: [] }), loading = ref(true), notFound = ref(false)
const allEvents = ref([]), loadingAll = ref(false)

const plannedEvents  = computed(() => allEvents.value.filter(e => e.status === 'planned'))
const activeEvents   = computed(() => allEvents.value.filter(e => e.status === 'active'))
const inactiveEvents = computed(() => allEvents.value.filter(e => e.status === 'inactive'))

function statusColor(s) {
  return s === 'planned' ? 'success' : s === 'active' ? 'primary' : 'grey'
}
function statusLabel(s) {
  return { planned: 'Регистрация открыта', active: 'Идёт', inactive: 'Завершено' }[s] || s
}
function formatDate(d) {
  if (!d) return ''
  const months = ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря']
  const [y, m, day] = d.split('-')
  return `${parseInt(day)} ${months[parseInt(m) - 1]} ${y}`
}

async function loadAll() {
  loadingAll.value = true
  try {
    const res = await api.get('/events?all=1')
    allEvents.value = res.data
  } catch { /* ignore */ } finally {
    loadingAll.value = false
  }
}

onMounted(async () => {
  if (route.params.slug === 'all') {
    notFound.value = true
    loading.value = false
    await loadAll()
    return
  }
  try {
    const res = await api.get(`/events/${route.params.slug}`)
    event.value = res.data
  } catch {
    notFound.value = true
    await loadAll()
  } finally {
    loading.value = false
  }
})

function goRegister(caseId) {
  if (!user.value) { router.push('/login'); return }
  router.push({ path: `/events/${route.params.slug}/register`, query: { case_id: caseId } })
}
</script>

<style scoped>
.case-card {
  background: var(--c-card-bg) !important;
  border: 1px solid var(--c-card-border) !important;
  height: 100%;
  transition: border-color 0.25s, box-shadow 0.25s, transform 0.25s;
}
.case-card:hover {
  border-color: var(--c-card-border-hover) !important;
  box-shadow: 0 0 24px var(--c-card-glow) !important;
  transform: translateY(-3px);
}
.spots-text { font-size: 0.78rem; color: var(--c-text-muted); }

.section-label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: var(--c-text-muted);
}

.events-list { display: flex; flex-direction: column; gap: 8px; }

.event-row {
  border: 1px solid var(--c-card-border);
  border-left: 3px solid #3a3a78;
  padding: 11px 14px;
  cursor: pointer;
  background: var(--c-card-bg);
  border-radius: 0 4px 4px 0;
  transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
}
.event-row:hover {
  border-color: var(--c-card-border-hover);
  border-left-color: #5858c8;
  box-shadow: 0 0 16px var(--c-card-glow);
  transform: translateX(2px);
}
.event-row--active   { border-left-color: #3a6aa8; }
.event-row--active:hover { border-left-color: #5588cc; }
.event-row--inactive { border-left-color: #888; opacity: 0.72; }
.event-row--inactive:hover { border-left-color: #aaa; }

.event-meta--date { color: #2a7a2a; font-weight: 600; }

.start-date-hint {
  font-size: 13px;
  color: var(--c-text-dim);
  display: flex;
  align-items: center;
}

.event-header { display: flex; align-items: center; margin-bottom: 5px; }

.event-title { font-size: 14px; font-weight: 600; color: #1a1aaa; flex: 1; }
.event-title--inactive { color: #555; }

.event-desc { font-size: 12px; color: var(--c-text-dim); line-height: 1.52; margin: 0 0 8px; }

.event-footer {
  display: flex; align-items: center; gap: 14px;
  font-size: 11px; color: var(--c-text-muted);
}
.event-meta { display: flex; align-items: center; gap: 3px; }

.event-more {
  margin-left: auto; color: #1a1aaa;
  text-decoration: none; font-size: 11px; cursor: pointer;
}
.event-more:hover { text-decoration: underline; }

.empty-msg { font-size: 13px; color: var(--c-text-muted); }
</style>
