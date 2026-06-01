<template>
  <div class="home">

    
    <section class="hero-section">
      <div class="hero-inner">

        <div class="hero-brand anim-slide-down">
          <span class="hero-logo-text">NYX</span>
          <span class="hero-logo-tagline">Team&nbsp;Platform</span>
        </div>

        <div class="hero-cta-row anim-fade-up delay-1">
          <v-btn color="secondary" variant="flat" size="large" to="/signup" rounded="sm">
            Зарегистрировать команду
          </v-btn>
          <v-btn variant="outlined" size="large" to="/events/practice-2025-2026" rounded="sm" class="hero-btn-out">
            Смотреть мероприятия
          </v-btn>
        </div>

        <p class="hero-hint anim-fade-up delay-2">
          {{ stats.events }} активных события · {{ stats.cases }} открытых кейсов · {{ stats.teams }} команд
        </p>

      </div>
    </section>

    
    <v-container class="py-5">
      <v-row>

        
        <v-col cols="12" md="8">

          
          <v-card class="home-card mb-4 anim-fade-up" :elevation="0">
            <v-card-text class="pa-5">
              <p class="desc-text">
                <strong>NYX</strong> — некоммерческая платформа для проведения IT-мероприятий.
                Здесь команды из школьников и студентов решают реальные технические задачи,
                предложенные организаторами соревнований.
              </p>
              <v-divider class="my-3" />
              <div class="desc-features">
                <div v-for="feat in features" :key="feat.title" class="desc-feature">
                  <span class="desc-feature-title">{{ feat.title }}</span>
                  <span class="desc-feature-body">{{ feat.body }}</span>
                </div>
              </div>
            </v-card-text>
          </v-card>

          
          <v-card class="home-card anim-fade-up delay-1" :elevation="0">
            <v-card-title class="pa-5 pb-2 card-section-title">Активные мероприятия</v-card-title>
            <v-divider />
            <v-card-text class="pa-4">

              <div v-if="loading" class="text-center py-8">
                <v-progress-circular indeterminate color="secondary" size="36" />
              </div>

              <div v-else-if="!displayedEvents.length" class="text-center py-8 empty-msg">
                <v-icon size="36" class="mb-2">mdi-calendar-blank-outline</v-icon>
                <p>Активных мероприятий пока нет</p>
              </div>

              <div v-else class="events-list">
                <div
                  v-for="ev in displayedEvents"
                  :key="ev.id || ev.slug"
                  class="event-row"
                  @click="$router.push('/events/' + (ev.slug || 'practice-2025-2026'))"
                >
                  <div class="event-header">
                    <v-icon size="14" color="secondary" class="mr-1">mdi-calendar-star</v-icon>
                    <span class="event-title">{{ ev.name || ev.title }}</span>
                    <v-chip color="success" variant="tonal" size="x-small" class="ml-2">ОТКРЫТО</v-chip>
                  </div>
                  <p class="event-desc">{{ ev.description }}</p>
                  <div class="event-footer">
                    <span class="event-meta">
                      <v-icon size="11">mdi-briefcase-outline</v-icon>
                      {{ ev.cases_count || 0 }}&nbsp;кейсов
                    </span>
                    <span class="event-meta">
                      <v-icon size="11">mdi-map-marker-outline</v-icon>
                      {{ ev.location || 'IT Cube' }}
                    </span>
                    <a class="event-more" @click.stop="$router.push('/events/' + (ev.slug || 'practice-2025-2026'))">
                      Подробнее&nbsp;→
                    </a>
                  </div>
                </div>
              </div>

            </v-card-text>
          </v-card>

        </v-col>

        
        <v-col cols="12" md="4">

          <v-card class="home-card mb-4 anim-fade-up delay-2" :elevation="0">
            <v-card-title class="pa-4 pb-2 card-section-title">Новости платформы</v-card-title>
            <v-divider />
            <v-card-text class="pa-3">
              <div class="news-list">
                <div v-for="n in news" :key="n.id" class="news-item">
                  <a href="#" class="news-link">{{ n.text }}</a>
                </div>
              </div>
            </v-card-text>
          </v-card>

          <v-card class="home-card anim-fade-up delay-3" :elevation="0">
            <v-card-title class="pa-4 pb-2 card-section-title">Статистика</v-card-title>
            <v-divider />
            <v-card-text class="pa-3">
              <table class="stats-tbl">
                <tr v-for="r in statsRows" :key="r.label">
                  <td class="tbl-label">{{ r.label }}</td>
                  <td class="tbl-val">{{ r.value }}</td>
                </tr>
              </table>
            </v-card-text>
          </v-card>

        </v-col>

      </v-row>
    </v-container>

    
    <section class="onboard-section">
      <v-container>
        <h2 class="onboard-title">Впервые на NYX?</h2>
        <v-row>
          <v-col
            v-for="(step, i) in steps"
            :key="step.label"
            cols="12" sm="6" md="3"
            :class="`anim-fade-up delay-${i + 1}`"
          >
            <v-card class="home-card onboard-card" :elevation="0" height="100%">
              <v-card-text class="text-center pa-5 d-flex flex-column align-center">
                <v-icon :color="step.color" size="32" class="mb-3">{{ step.icon }}</v-icon>
                <strong class="onboard-card-title d-block mb-2">{{ step.label }}</strong>
                <p class="onboard-card-desc">{{ step.desc }}</p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    
    <footer class="site-footer">
      <span>© 2026 NYX Team Platform</span>
      <span class="fp">|</span>
      <a href="#">О платформе</a>
      <span class="fp">|</span>

      <div class="footer-dropdown">
        <a href="#" class="footer-dropdown-trigger" @click.prevent="toggleContacts">
          Контакты <span class="footer-arrow">▾</span>
        </a>
        <div v-if="contactsOpen" class="footer-dropdown-menu">
          <a href="mailto:info@nyx-team.ru" class="footer-dropdown-item">
            <v-icon size="13">mdi-email-outline</v-icon> info@nyx-team.ru
          </a>
          <a href="https://t.me/nyx_team" class="footer-dropdown-item">
            <v-icon size="13">mdi-send</v-icon> Telegram
          </a>
          <a href="#" class="footer-dropdown-item">
            <v-icon size="13">mdi-office-building-outline</v-icon> IT Cube, ул. Примерная, 1
          </a>
        </div>
      </div>

      <span class="fp">|</span>

      <div class="footer-dropdown">
        <a href="#" class="footer-dropdown-trigger" @click.prevent="toggleHelp">
          Помощь <span class="footer-arrow">▾</span>
        </a>
        <div v-if="helpOpen" class="footer-dropdown-menu">
          <a href="#" class="footer-dropdown-item">
            <v-icon size="13">mdi-book-open-outline</v-icon> Инструкция по регистрации
          </a>
          <a href="#" class="footer-dropdown-item">
            <v-icon size="13">mdi-frequently-asked-questions</v-icon> Частые вопросы
          </a>
          <a href="#" class="footer-dropdown-item">
            <v-icon size="13">mdi-bug-outline</v-icon> Сообщить об ошибке
          </a>
        </div>
      </div>

      <span class="fp">|</span>
      <a href="/admin/login">Администратор</a>
    </footer>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api.js'
import { events } from '../stores/events.js'

const router = useRouter()
const loading      = ref(true)
const contactsOpen = ref(false)
const helpOpen     = ref(false)

function toggleContacts() { contactsOpen.value = !contactsOpen.value; helpOpen.value = false }
function toggleHelp()     { helpOpen.value     = !helpOpen.value;     contactsOpen.value = false }

const localEvents = ref([])
const stats = ref({ events: 0, cases: 0, teams: 0, members: 0 })

const features = [
  { title: 'Регистрация команды',          body: 'Создайте профиль, пригласите участников по коду и назначьте капитана команды.' },
  { title: 'Выбор кейса',                  body: 'Каждое мероприятие предлагает несколько кейсов разных направлений — выберите тот, что ближе вашей команде.' },
  { title: 'Личный кабинет',               body: 'Отслеживайте статус команды, меняйте данные участников и переключайтесь между кейсами.' },
  { title: 'Управление для организаторов', body: 'Администраторы создают события, устанавливают лимиты и выгружают списки команд в один клик.' },
]

const news = [
  { id: 1, text: 'Открыта регистрация на IT Cube Case 2025–2026' },
  { id: 2, text: 'Добавлены новые кейсы по машинному обучению' },
  { id: 3, text: 'Обновление: доступна смена кейса команды' },
  { id: 4, text: 'Итоги прошлогоднего соревнования опубликованы' },
]

const statsRows = computed(() => [
  { label: 'Активных событий',  value: String(stats.value.events)             },
  { label: 'Открытых кейсов',   value: String(stats.value.cases)              },
  { label: 'Зарегистрировано',  value: `${stats.value.teams} команд`          },
  { label: 'Всего участников',  value: String(stats.value.members)            },
])

const steps = [
  { icon: 'mdi-account-plus-outline', color: '#1a5a96', label: 'Регистрация',   desc: 'Создайте аккаунт и сформируйте команду из участников'      },
  { icon: 'mdi-calendar-check',       color: '#2e7d32', label: 'Выбор события', desc: 'Найдите подходящее соревнование в списке мероприятий'       },
  { icon: 'mdi-briefcase-check',      color: '#c87800', label: 'Выбор кейса',   desc: 'Запишитесь на интересный кейс внутри выбранного события'    },
  { icon: 'mdi-trophy',               color: '#b71c1c', label: 'Участие',       desc: 'Решайте задачи, сотрудничайте с командой и побеждайте!'     },
]

onMounted(async () => {
  try {
    const [evRes, stRes] = await Promise.all([
      api.get('/events'),
      api.get('/stats'),
    ])
    localEvents.value = evRes.data
    stats.value = stRes.data
  } catch {
    localEvents.value = []
  } finally {
    loading.value = false
  }
})

const displayedEvents = computed(() => {
  if (localEvents.value.length > 0) return localEvents.value
  return events.value
    .filter(e => e.status === 'active')
    .map(e => ({ ...e, title: e.name || e.title }))
})
</script>

<style scoped>
/* ROOT */
.home {
  min-height: 100vh;
  background: var(--c-page-bg);
  font-family: Arial, Helvetica, sans-serif;
  color: #111;
}

/* ═══════════ HERO ═══════════ */
.hero-section {
  background: linear-gradient(180deg, #2e2e42 0%, #1e1e2e 100%);
  border-bottom: 2px solid #111120;
  padding: 42px 20px 36px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.45);
}

.hero-inner {
  max-width: 760px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 22px;
}

.hero-brand {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.hero-logo-text {
  font-family: 'PT Serif', Georgia, 'Times New Roman', serif;
  font-size: 60px;
  font-weight: 700;
  color: #e8e8f4;
  letter-spacing: 16px;
  line-height: 1;
  text-shadow:
    1px 1px 0 rgba(0, 0, 0, 0.6),
    0 0 28px rgba(140, 140, 230, 0.22);
}

.hero-logo-tagline {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 10px;
  font-weight: 600;
  color: #6868a0;
  letter-spacing: 6px;
  text-transform: uppercase;
}

.hero-cta-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
}

.hero-btn-out {
  color: #98b8de !important;
  border-color: #485898 !important;
}

.hero-hint {
  font-size: 12px;
  color: #5858a0;
  font-style: italic;
}

/* ═══════════ CARDS — identical to EventPage .case-card ═══════════ */
.home-card {
  background: var(--c-card-bg) !important;
  border: 1px solid var(--c-card-border) !important;
  border-radius: 4px !important;
  transition: border-color 0.25s, box-shadow 0.25s;
}

.home-card:hover {
  border-color: var(--c-card-border-hover) !important;
  box-shadow: 0 0 24px var(--c-card-glow) !important;
}

.card-section-title {
  font-family: 'PT Serif', Georgia, Times, serif;
  font-size: 15px !important;
  font-weight: 700 !important;
  color: #1a1a28;
  letter-spacing: 0.2px;
}

/* ═══════════ DESCRIPTION ═══════════ */
.desc-text {
  font-family: 'PT Serif', Georgia, Times, serif;
  font-size: 14px;
  line-height: 1.7;
  color: #1a1a1a;
  margin: 0;
}

.desc-features {
  display: flex;
  flex-direction: column;
}

.desc-feature {
  display: grid;
  grid-template-columns: 190px 1fr;
  gap: 0 14px;
  padding: 8px 0;
  border-bottom: 1px solid var(--c-card-border);
  align-items: baseline;
}

.desc-feature:last-child { border-bottom: none; }

.desc-feature-title {
  font-size: 13px;
  font-weight: 700;
  color: #1a1a6a;
}

.desc-feature-body {
  font-size: 12px;
  color: var(--c-text-dim);
  line-height: 1.52;
}

/* ═══════════ EVENTS LIST ═══════════ */
.events-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

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

.event-header {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.event-title {
  font-size: 14px;
  font-weight: 600;
  color: #1a1aaa;
  flex: 1;
}

.event-desc {
  font-size: 12px;
  color: var(--c-text-dim);
  line-height: 1.52;
  margin: 0 0 8px;
}

.event-footer {
  display: flex;
  align-items: center;
  gap: 14px;
  font-size: 11px;
  color: var(--c-text-muted);
}

.event-meta {
  display: flex;
  align-items: center;
  gap: 3px;
}

.event-more {
  margin-left: auto;
  color: #1a1aaa;
  text-decoration: none;
  font-size: 11px;
  cursor: pointer;
}

.event-more:hover { text-decoration: underline; }

.empty-msg { color: var(--c-text-muted); font-size: 13px; }

/* ═══════════ SIDEBAR ═══════════ */
.news-item {
  padding: 6px 0;
  border-bottom: 1px solid var(--c-card-border);
}

.news-item:last-child { border-bottom: none; }

.news-link {
  font-size: 12px;
  color: #1a0dab;
  text-decoration: none;
  line-height: 1.4;
}

.news-link:hover { text-decoration: underline; }

.stats-tbl {
  width: 100%;
  border-collapse: collapse;
}

.tbl-label {
  font-size: 11px;
  color: var(--c-text-dim);
  padding: 5px 4px 5px 0;
  border-bottom: 1px solid var(--c-card-border);
}

.tbl-val {
  font-size: 11px;
  font-weight: 700;
  color: #1a1a8a;
  text-align: right;
  padding: 5px 0;
  border-bottom: 1px solid var(--c-card-border);
  white-space: nowrap;
}

/* ═══════════ ONBOARDING ═══════════ */
.onboard-section {
  background: var(--c-page-bg);
  border-top: 1px solid #b8b8c4;
  padding: 28px 0;
}

.onboard-title {
  font-family: 'PT Serif', Georgia, Times, serif;
  font-size: 20px;
  font-weight: 700;
  color: #1a1a28;
  text-align: center;
  margin: 0 0 20px;
}

.onboard-card {
  transition: border-color 0.25s, box-shadow 0.25s, transform 0.25s !important;
}

.onboard-card:hover {
  transform: translateY(-3px) !important;
}

.onboard-card-title {
  font-family: 'PT Serif', Georgia, Times, serif;
  font-size: 13px;
  color: #1a1a6a;
}

.onboard-card-desc {
  font-size: 11px;
  color: var(--c-text-dim);
  line-height: 1.5;
  margin: 0;
}

/* ═══════════ FOOTER ═══════════ */
.site-footer {
  background: linear-gradient(180deg, #d0d0d0 0%, #c4c4c4 100%);
  border-top: 1px solid #aaaaaa;
  padding: 10px 16px;
  text-align: center;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 11px;
  color: #555;
}

.site-footer a {
  color: #1a4a8a;
  text-decoration: none;
}

.site-footer a:hover { text-decoration: underline; }

.fp { margin: 0 7px; color: #aaaaaa; }

.footer-dropdown {
  position: relative;
  display: inline-block;
}

.footer-dropdown-trigger {
  color: #1a4a8a;
  text-decoration: none;
  font-size: 11px;
  cursor: pointer;
  user-select: none;
}

.footer-dropdown-trigger:hover { text-decoration: underline; }

.footer-arrow { font-size: 9px; vertical-align: middle; }

.footer-dropdown-menu {
  position: absolute;
  bottom: calc(100% + 6px);
  left: 50%;
  transform: translateX(-50%);
  background: var(--c-card-bg);
  border: 1px solid var(--c-card-border);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.18);
  border-radius: 4px;
  min-width: 210px;
  z-index: 100;
  white-space: nowrap;
}

.footer-dropdown-item {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 7px 12px;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 12px;
  color: #1a1a1a !important;
  text-decoration: none !important;
  border-bottom: 1px solid var(--c-card-border);
  transition: background 0.1s;
}

.footer-dropdown-item:last-child { border-bottom: none; }

.footer-dropdown-item:hover {
  background: var(--c-hint-bg);
  color: #1a1a8a !important;
  text-decoration: none !important;
}

/* ═══════════ RESPONSIVE ═══════════ */
@media (max-width: 600px) {
  .hero-logo-text { font-size: 48px; letter-spacing: 10px; }
  .desc-feature { grid-template-columns: 1fr; gap: 2px; }
  .onboard-title { font-size: 17px; }
}
</style>
