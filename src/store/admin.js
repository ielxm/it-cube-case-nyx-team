import { ref } from 'vue'
import api from '../api.js'
import {
  events, cases, fetchAll,
  createEvent as createEventStore, updateEvent as updateEventStore, deleteEvent as deleteEventStore,
  createCase  as createCaseStore,  updateCase  as updateCaseStore,  deleteCase  as deleteCaseStore,
} from '../stores/events.js'

const admin        = ref(JSON.parse(localStorage.getItem('admin')  || 'null'))
const adminToken   = ref(localStorage.getItem('adminToken')        || null)
const pendingToken = ref(sessionStorage.getItem('adminPendingToken') || null)

const mockEvents      = events
const mockCases       = cases
const mockTeams       = ref([])
const mockInviteCodes = ref([])
const adminsList      = ref([])
const newsList        = ref([])

async function loginAdmin(email, password) {
  const res = await api.post('/admin/auth/login', { email, password })
  pendingToken.value = res.data.pending_token
  admin.value = { email: res.data.email }
  sessionStorage.setItem('adminPendingToken', res.data.pending_token)
  localStorage.setItem('admin', JSON.stringify(admin.value))
  return true
}

async function verifyTOTP(code) {
  const res = await api.post('/admin/auth/verify-totp', {
    pending_token: pendingToken.value,
    code,
  })
  adminToken.value = res.data.token
  admin.value = { email: res.data.email, name: res.data.name }
  localStorage.setItem('adminToken', res.data.token)
  localStorage.setItem('admin', JSON.stringify(admin.value))
  sessionStorage.removeItem('adminPendingToken')
  pendingToken.value = null
  return true
}

async function resendTOTP() {
  await api.post('/admin/auth/resend-totp', null, {
    params: { pending_token: pendingToken.value },
  })
}

function logoutAdmin() {
  admin.value      = null
  adminToken.value = null
  localStorage.removeItem('adminToken')
  localStorage.removeItem('admin')
  sessionStorage.removeItem('adminPendingToken')
}

async function fetchAdminsList() {
  const res      = await api.get('/admin/auth/admins')
  adminsList.value = res.data
}

async function createAdminAccount(data) {
  await api.post('/admin/auth/create', data)
  await fetchAdminsList()
}

async function deleteAdminAccount(id) {
  await api.delete(`/admin/auth/admins/${id}`)
  await fetchAdminsList()
}

async function fetchTeams() {
  try {
    const res       = await api.get('/admin/teams')
    mockTeams.value = res.data
  } catch (e) {
    console.error('Ошибка загрузки команд:', e)
  }
}

async function fetchInviteCodes(eventId = null) {
  try {
    const params          = eventId ? { event_id: eventId } : {}
    const res             = await api.get('/invite-codes', { params })
    mockInviteCodes.value = res.data
  } catch (e) {
    console.error('Ошибка загрузки кодов:', e)
  }
}

async function generateInviteCode(eventId, count = 1) {
  const created = []
  for (let i = 0; i < count; i++) {
    const code = Math.random().toString(36).substring(2, 8).toUpperCase()
    try {
      const res = await api.post('/invite-codes', { code, event_id: eventId })
      mockInviteCodes.value.push(res.data)
      created.push(code)
    } catch (e) {
      console.error('Ошибка создания кода:', e)
    }
  }
  return created
}

async function addInviteCode(code, eventId) {
  try {
    const res = await api.post('/invite-codes', { code, event_id: eventId })
    mockInviteCodes.value.push(res.data)
    return res.data
  } catch (e) {
    const msg = e.response?.data?.detail || 'Ошибка добавления кода'
    throw new Error(msg)
  }
}

function createEvent(data)     { return createEventStore(data) }
function updateEvent(id, data) { return updateEventStore(id, data) }
function deleteEvent(id)       { return deleteEventStore(id) }
function createCase(data)      { return createCaseStore(data) }
function updateCase(id, data)  { return updateCaseStore(id, data) }
function deleteCase(id)        { return deleteCaseStore(id) }

async function fetchNews() {
  const res      = await api.get('/news')
  newsList.value = res.data
}

async function createNews(text) {
  const res = await api.post('/news', { text })
  newsList.value.unshift(res.data)
}

async function deleteNews(id) {
  await api.delete(`/news/${id}`)
  newsList.value = newsList.value.filter(n => n.id !== id)
}

async function fetchAdminStats() {
  const res = await api.get('/admin/stats')
  return res.data
}

function exportToCSV(data, filename) {
  let csv = ''
  if (filename.includes('stats')) {
    csv = 'Кейс,Лимит,Занято,Свободно\n'
    data.cases.forEach(c => {
      csv += `"${c.title}",${c.limit_teams},${c.registered},${c.limit_teams - c.registered}\n`
    })
  } else if (filename.includes('teams')) {
    csv = 'ID,Название,Лидер,Мероприятие,Кейс,Участников,Код\n'
    data.forEach(t => {
      csv += `${t.id},"${t.name}","${t.leader_name || ''}","${t.event_title || ''}","${t.case_title || ''}",${t.member_count || 0},${t.team_code}\n`
    })
  }
  const blob = new Blob(['﻿' + csv], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.setAttribute('download', filename)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

export {
  admin, adminToken, pendingToken,
  mockEvents, mockCases, mockTeams, mockInviteCodes, adminsList, newsList,
  loginAdmin, verifyTOTP, resendTOTP, logoutAdmin,
  fetchAdminsList, createAdminAccount, deleteAdminAccount,
  fetchAll, fetchTeams, fetchInviteCodes, generateInviteCode, addInviteCode,
  createEvent, updateEvent, deleteEvent,
  createCase, updateCase, deleteCase,
  fetchAdminStats, exportToCSV,
  fetchNews, createNews, deleteNews,
}
