<template>
  <v-app>
    <NavBar />
    <v-main>
      <RouterView v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </v-main>
  </v-app>
</template>

<script setup>
import NavBar from './components/NavBar.vue'
</script>

<style>
/* ─── CSS-переменные для тёмной темы ─── */
.v-theme--dark {
  --c-page-bg:          #08060f;
  --c-card-bg:          #110e24;
  --c-nav-bg:           rgba(8, 6, 15, 0.95);
  --c-nav-border:       rgba(109, 40, 217, 0.25);
  --c-card-border:      rgba(109, 40, 217, 0.25);
  --c-card-border-hover:rgba(167, 139, 250, 0.6);
  --c-card-glow:        rgba(109, 40, 217, 0.15);
  --c-hero-title:       #a78bfa;
  --c-hero-orb1:        rgba(109, 40, 217, 0.18);
  --c-hero-orb2:        rgba(167, 139, 250, 0.10);
  --c-text-dim:         rgba(255, 255, 255, 0.55);
  --c-text-muted:       rgba(255, 255, 255, 0.40);
  --c-hint-bg:          rgba(109, 40, 217, 0.07);
  --c-hint-border:      rgba(109, 40, 217, 0.20);
  --c-cred-bg:          rgba(109, 40, 217, 0.10);
  --c-cred-border:      rgba(109, 40, 217, 0.30);
}

/* ─── CSS-переменные для светлой темы ─── */
.v-theme--light {
  --c-page-bg:          #f5f3ff;
  --c-card-bg:          #ffffff;
  --c-nav-bg:           rgba(255, 255, 255, 0.95);
  --c-nav-border:       rgba(109, 40, 217, 0.15);
  --c-card-border:      rgba(109, 40, 217, 0.18);
  --c-card-border-hover:rgba(109, 40, 217, 0.55);
  --c-card-glow:        rgba(109, 40, 217, 0.10);
  --c-hero-title:       #6d28d9;
  --c-hero-orb1:        rgba(109, 40, 217, 0.08);
  --c-hero-orb2:        rgba(167, 139, 250, 0.07);
  --c-text-dim:         rgba(0, 0, 0, 0.60);
  --c-text-muted:       rgba(0, 0, 0, 0.45);
  --c-hint-bg:          rgba(109, 40, 217, 0.04);
  --c-hint-border:      rgba(109, 40, 217, 0.15);
  --c-cred-bg:          rgba(109, 40, 217, 0.05);
  --c-cred-border:      rgba(109, 40, 217, 0.20);
}

/* ─── Глобальные стили ─── */
body, .v-application, .v-main {
  background-color: var(--c-page-bg) !important;
  font-family: 'Roboto', sans-serif;
}
a { color: inherit; text-decoration: none; }

/* ─── Переходы между страницами ─── */
.page-enter-active { transition: opacity 0.35s ease, transform 0.35s ease; }
.page-leave-active { transition: opacity 0.2s ease; }
.page-enter-from   { opacity: 0; transform: translateY(16px); }
.page-leave-to     { opacity: 0; }

/* ─── Общие анимации (используются во всех страницах) ─── */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes popIn {
  0%   { opacity: 0; transform: scale(0.85); }
  70%  { transform: scale(1.04); }
  100% { opacity: 1; transform: scale(1); }
}
@keyframes slideDown {
  from { opacity: 0; transform: translateY(-20px); }
  to   { opacity: 1; transform: translateY(0); }
}

.anim-fade-up    { animation: fadeUp   0.5s ease both; }
.anim-fade-in    { animation: fadeIn   0.5s ease both; }
.anim-pop-in     { animation: popIn    0.4s ease both; }
.anim-slide-down { animation: slideDown 0.4s ease both; }

.delay-1 { animation-delay: 0.10s; }
.delay-2 { animation-delay: 0.20s; }
.delay-3 { animation-delay: 0.30s; }
.delay-4 { animation-delay: 0.40s; }
.delay-5 { animation-delay: 0.50s; }
.delay-6 { animation-delay: 0.60s; }
</style>
