<template>
  <v-app-bar flat :height="64" class="archive-nav">

    <div class="arch-inner">

      
      <router-link to="/" class="arch-logo">
        <div class="arch-logo-icon-wrap">
          <v-icon color="#b8b8d0" size="34">mdi-archive-outline</v-icon>
        </div>
        <div class="arch-logo-text">
          <span class="arch-logo-main">NYX</span>
          <span class="arch-logo-sub">TEAM</span>
        </div>
      </router-link>

      
      <div class="arch-vr"></div>

      
      <nav class="arch-tabs">
        <router-link
          v-for="tab in tabs"
          :key="tab.to"
          :to="tab.to"
          class="arch-tab"
          :class="{ 'arch-tab--active': isActive(tab) }"
        >
          <v-icon class="arch-tab-ico" size="20">{{ tab.icon }}</v-icon>
          <span class="arch-tab-lbl">{{ tab.label }}</span>
        </router-link>
      </nav>

      <div class="arch-spacer"></div>

      
      <div class="arch-auth">
        <template v-if="!user">
          <router-link to="/signup" class="arch-auth-link">РЕГИСТРАЦИЯ</router-link>
          <span class="arch-pipe">|</span>
          <router-link to="/login" class="arch-auth-link">ВОЙТИ</router-link>
        </template>
        <template v-else>
          <span class="arch-user-name">
            <v-icon size="13" style="margin-right:3px; vertical-align:middle;">mdi-account-circle</v-icon>
            {{ user.full_name }}
          </span>
          <span class="arch-pipe">|</span>
          <router-link to="/dashboard" class="arch-auth-link">КАБИНЕТ</router-link>
          <span class="arch-pipe">|</span>
          <a href="#" class="arch-auth-link" @click.prevent="doLogout">ВЫЙТИ</a>
        </template>
      </div>

    </div>
  </v-app-bar>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { user, logout } from '../store/auth.js'

const route  = useRoute()
const router = useRouter()

const tabs = [
  { to: '/',                          icon: 'mdi-web',               label: 'ГЛАВНАЯ'  },
  { to: '/events/practice-2025-2026', icon: 'mdi-book-open-variant', label: 'СОБЫТИЯ'  },
]

function isActive(tab) {
  if (!tab.to) return false
  if (tab.to === '/') return route.path === '/'
  return route.path.startsWith(tab.to)
}

function doLogout() {
  logout()
  router.push('/')
}
</script>

<style scoped>
.arch-inner {
  display: flex;
  align-items: center;
  width: 100%;
  height: 100%;
  padding: 0 16px;
  max-width: 1300px;
  margin: 0 auto;
}

/* ── Logo ── */
.arch-logo {
  display: flex;
  align-items: center;
  gap: 9px;
  text-decoration: none;
  padding-right: 16px;
  flex-shrink: 0;
  cursor: pointer;
}

.arch-logo-icon-wrap {
  filter: drop-shadow(0 0 6px rgba(140, 140, 210, 0.35));
  display: flex;
  align-items: center;
}

.arch-logo-text {
  display: flex;
  flex-direction: column;
  line-height: 1;
  gap: 2px;
}

.arch-logo-main {
  font-family: 'PT Serif', Georgia, 'Times New Roman', serif;
  font-size: 21px;
  font-weight: 700;
  color: #e8e8f4;
  letter-spacing: 5px;
  text-shadow:
    1px 1px 0 rgba(0, 0, 0, 0.75),
    0 0 14px rgba(150, 150, 240, 0.20);
}

.arch-logo-sub {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 8px;
  font-weight: 400;
  color: #606080;
  letter-spacing: 4px;
  text-transform: uppercase;
}

/* ── Vertical rule ── */
.arch-vr {
  width: 1px;
  height: 32px;
  background: linear-gradient(180deg, transparent, rgba(255,255,255,0.12) 25%, rgba(255,255,255,0.12) 75%, transparent);
  margin: 0 8px;
  flex-shrink: 0;
}

/* ── Tabs ── */
.arch-tabs {
  display: flex;
  align-items: stretch;
  height: 64px;
  flex-shrink: 0;
  gap: 2px;
}

.arch-tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 0 18px;
  cursor: pointer;
  text-decoration: none;
  color: #7878a0;
  position: relative;
  transition: color 0.15s, background 0.15s;
  min-width: 78px;
  border-radius: 2px 2px 0 0;
  user-select: none;
}

.arch-tab:hover {
  color: #d4d4f4;
  background: rgba(255, 255, 255, 0.06);
}

.arch-tab--active {
  color: #ffffff !important;
  background: rgba(255, 255, 255, 0.09) !important;
}

.arch-tab--active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #5858c8, #9898ec, #5858c8);
  box-shadow: 0 0 8px rgba(110, 110, 240, 0.50);
  border-radius: 2px 2px 0 0;
}

.arch-tab-ico {
  color: inherit !important;
}

.arch-tab-lbl {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1px;
  color: inherit;
  white-space: nowrap;
}

/* ── Spacer ── */
.arch-spacer { flex: 1 1 0; }

/* ── Auth ── */
.arch-auth {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-left: 16px;
  border-left: 1px solid rgba(255, 255, 255, 0.07);
  flex-shrink: 0;
}

.arch-auth-link {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 11px;
  font-weight: 600;
  color: #b0b0cc;
  text-decoration: none;
  letter-spacing: 0.5px;
  white-space: nowrap;
  transition: color 0.12s;
}

.arch-auth-link:hover {
  color: #ffffff;
  text-decoration: underline;
}

.arch-pipe {
  color: #404055;
  font-size: 13px;
  user-select: none;
  line-height: 1;
}

.arch-user-name {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 11px;
  color: #88a8cc;
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
