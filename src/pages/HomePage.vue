<template>
  <div>

    <!-- ===== Герой ===== -->
    <div class="hero">
      <div class="glow-orb orb-1" />
      <div class="glow-orb orb-2" />

      <h1 class="hero-title anim-fade-up">Nyx!</h1>

      <!-- Главный слоган -->
      <p class="hero-slogan anim-fade-up delay-1">Попробуй себя в роли разработчика!</p>
      <p class="hero-desc anim-fade-up delay-2">
        Выбирайте мероприятия, регистрируйте команды и управляйте заявками в одном месте
      </p>

      <div class="anim-fade-up delay-3">
        <v-btn color="secondary" variant="flat" to="/signup" size="large" class="hero-btn mr-3">
          Начать участие
        </v-btn>
        <v-btn color="secondary" variant="outlined" to="/events/practice-2025-2026" size="large">
          Смотреть мероприятия
        </v-btn>
      </div>
    </div>

    <!-- ===== Список мероприятий ===== -->
    <v-container class="pb-10">
      <h2 class="section-title mb-5 anim-fade-up">Актуальные мероприятия</h2>

      <div v-if="loading" class="text-center py-12">
        <v-progress-circular indeterminate color="secondary" size="48" />
      </div>

      <v-row v-else-if="displayedEvents.length">
        <v-col v-for="(event, i) in displayedEvents" :key="event.id" cols="12" md="6"
               :class="`anim-fade-up delay-${i + 1}`">
          <v-card class="event-card" @click="$router.push(`/events/${event.slug}`)">
            <v-card-title class="text-h6 pt-5 px-5">{{ event.title }}</v-card-title>
            <v-card-text class="px-5" style="color: var(--c-text-dim);">{{ event.description }}</v-card-text>
            <v-card-actions class="px-5 pb-4">
              <v-chip color="success" size="small" variant="tonal">Идёт регистрация</v-chip>
              <v-spacer />
              <v-btn color="secondary" variant="text" append-icon="mdi-arrow-right" size="small">
                Подробнее
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <div v-else class="empty-state anim-fade-in">
        <v-icon size="64" color="secondary" class="mb-4">mdi-calendar-blank-outline</v-icon>
        <p>Активных мероприятий пока нет</p>
      </div>
    </v-container>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api.js'
import { events } from '../stores/events.js'

const localEvents  = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    // Пытаемся загрузить с API
    const res = await api.get('/events')
    localEvents.value = res.data
  } catch (e) {
    console.error('Не удалось загрузить мероприятия с API:', e)
    // Если API не работает, используем store данные
    localEvents.value = []
  } finally {
    loading.value = false
  }
})

// Если API не вернул данные, используем данные из store
const displayedEvents = computed(() => {
  if (localEvents.value.length > 0) {
    return localEvents.value
  }
  // Только активные мероприятия с полями title
  return events.value
    .filter(e => e.status === 'active')
    .map(e => ({
      ...e,
      title: e.name || e.title,
    }))
})
</script>

<style scoped>
.hero {
  position: relative;
  text-align: center;
  padding: 80px 20px 60px;
  overflow: hidden;
}

.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
}
.orb-1 {
  width: 400px; height: 400px;
  background: var(--c-hero-orb1);
  top: -100px; left: 50%;
  transform: translateX(-50%);
  animation: orbFloat 6s ease-in-out infinite;
}
.orb-2 {
  width: 250px; height: 250px;
  background: var(--c-hero-orb2);
  top: 40px; right: 10%;
  animation: orbFloat 8s ease-in-out infinite reverse;
}
@keyframes orbFloat {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50%       { transform: translateX(-50%) translateY(-20px); }
}

.hero-title {
  font-size: clamp(4rem, 14vw, 9rem);
  font-weight: 900;
  color: var(--c-hero-title);
  letter-spacing: 12px;
  margin: 0;
  line-height: 1;
  animation: fadeUp 0.6s ease both, glowPulse 4s ease-in-out infinite 0.6s;
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes glowPulse {
  0%, 100% { text-shadow: 0 0 80px rgba(109, 40, 217, 0.4); }
  50%       { text-shadow: 0 0 140px rgba(109, 40, 217, 0.8), 0 0 40px rgba(167, 139, 250, 0.4); }
}

.hero-slogan {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--c-hero-title);
  margin: 18px 0 8px;
  letter-spacing: 0.5px;
}
.hero-desc {
  color: var(--c-text-dim);
  font-size: 1rem;
  max-width: 480px;
  margin: 0 auto 30px;
  line-height: 1.6;
}

.hero-btn {
  transition: transform 0.15s, box-shadow 0.2s !important;
}
.hero-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(109, 40, 217, 0.4) !important;
}

.section-title { font-size: 1.4rem; font-weight: 700; }

.event-card {
  background: var(--c-card-bg) !important;
  border: 1px solid var(--c-card-border) !important;
  cursor: pointer;
  transition: border-color 0.25s, box-shadow 0.25s, transform 0.25s;
}
.event-card:hover {
  border-color: var(--c-card-border-hover) !important;
  box-shadow: 0 0 30px var(--c-card-glow) !important;
  transform: translateY(-3px);
}

.empty-state {
  text-align: center;
  padding: 80px 0;
  color: var(--c-text-muted);
}
</style>
