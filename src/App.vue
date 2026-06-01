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
/* ─── Global reset for archive theme ─── */
body, .v-application {
  font-family: Arial, Helvetica, sans-serif !important;
}

.v-application {
  background-color: #cccccc !important;
}

.v-main {
  padding-left: 0 !important;
  padding-right: 0 !important;
  background-color: #cccccc !important;
}

/* ─── Archive navbar override: applied globally so the class works ─── */
header.v-app-bar.archive-nav {
  background: linear-gradient(180deg, #353545 0%, #222232 100%) !important;
  border-bottom: 3px solid #111120 !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.55), inset 0 1px 0 rgba(100, 100, 160, 0.22) !important;
}

/* ─── CSS variables for other pages (login, signup, dashboard) ─── */
:root {
  --c-page-bg:         #cccccc;
  --c-card-bg:         #ffffff;
  --c-card-border:     #b8b8c0;
  --c-card-border-hover: #3a3a8a;
  --c-card-glow:       rgba(58, 58, 106, 0.12);
  --c-nav-bg:          #252535;
  --c-nav-border:      #111120;
  --c-hero-title:      #1a1a2a;
  --c-hero-orb1:       rgba(58, 58, 106, 0.10);
  --c-hero-orb2:       rgba(26, 90, 150, 0.08);
  --c-text-dim:        rgba(0, 0, 0, 0.58);
  --c-text-muted:      rgba(0, 0, 0, 0.40);
  --c-hint-bg:         rgba(58, 58, 106, 0.05);
  --c-hint-border:     rgba(58, 58, 106, 0.18);
  --c-cred-bg:         rgba(58, 58, 106, 0.06);
  --c-cred-border:     rgba(58, 58, 106, 0.22);
}

/* ─── Page transitions ─── */
.page-enter-active { transition: opacity 0.22s ease; }
.page-leave-active { transition: opacity 0.14s ease; }
.page-enter-from   { opacity: 0; }
.page-leave-to     { opacity: 0; }

/* ─── Shared animations ─── */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes popIn {
  0%   { opacity: 0; transform: scale(0.88); }
  70%  { transform: scale(1.03); }
  100% { opacity: 1; transform: scale(1); }
}
@keyframes slideDown {
  from { opacity: 0; transform: translateY(-14px); }
  to   { opacity: 1; transform: translateY(0); }
}

.anim-fade-up    { animation: fadeUp    0.45s ease both; }
.anim-fade-in    { animation: fadeIn    0.45s ease both; }
.anim-pop-in     { animation: popIn     0.38s ease both; }
.anim-slide-down { animation: slideDown 0.38s ease both; }

.delay-1 { animation-delay: 0.08s; }
.delay-2 { animation-delay: 0.16s; }
.delay-3 { animation-delay: 0.24s; }
.delay-4 { animation-delay: 0.32s; }
.delay-5 { animation-delay: 0.40s; }
.delay-6 { animation-delay: 0.48s; }
</style>
