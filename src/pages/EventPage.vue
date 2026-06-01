<template>
  <v-container class="py-8">
    <div v-if="loading" class="text-center py-16">
      <v-progress-circular indeterminate color="secondary" size="48" />
    </div>
    <div v-else>
      <v-btn variant="text" prepend-icon="mdi-arrow-left" to="/" class="mb-6 anim-fade-in" color="secondary">
        Все мероприятия
      </v-btn>
      <div class="mb-8 anim-fade-up">
        <h1 class="text-h4 font-weight-bold">{{ event.title }}</h1>
        <p class="mt-2 mb-3" style="max-width: 680px; line-height: 1.6; color: var(--c-text-dim);">{{ event.description }}</p>
        <v-chip color="success" variant="tonal">Регистрация открыта</v-chip>
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
              <v-chip :color="c.registered < c.limit_teams ? 'success' : 'error'" variant="tonal" size="small">
                {{ c.registered < c.limit_teams ? `Свободно ${c.limit_teams - c.registered} мест` : 'Мест нет' }}
              </v-chip>
              <v-spacer />
              <v-btn color="secondary" variant="flat" size="small"
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
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api.js'
import { user } from '../store/auth.js'

const route = useRoute(), router = useRouter()
const event = ref({ cases: [] }), loading = ref(true)

onMounted(async () => {
  try {
    const res = await api.get(`/events/${route.params.slug}`)
    event.value = res.data
  } catch { router.push('/') }
  finally { loading.value = false }
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
</style>
