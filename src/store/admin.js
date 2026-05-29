import { ref } from 'vue'
import { events, cases, createEvent as createEventStore, updateEvent as updateEventStore, deleteEvent as deleteEventStore, createCase as createCaseStore, updateCase as updateCaseStore, deleteCase as deleteCaseStore } from '../stores/events.js'

// Загружаем админ данные из localStorage
const admin = ref(JSON.parse(localStorage.getItem('admin') || 'null'))
const is2FAVerified = ref(localStorage.getItem('admin2FAVerified') === 'true')

// Используем глобальный store мероприятий
const mockEvents = events
const mockCases = cases

const mockTeams = ref([
  { id: 1, name: 'Команда 1', captain: 'Иван Иванов', email: 'ivan@example.com', phone: '+7 999 123-45-67', caseId: 1, status: 'active' },
  { id: 2, name: 'Команда 2', captain: 'Мария Петрова', email: 'maria@example.com', phone: '+7 999 234-56-78', caseId: 1, status: 'active' },
  { id: 3, name: 'Команда 3', captain: 'Петр Сидоров', email: 'petr@example.com', phone: '+7 999 345-67-89', caseId: 2, status: 'active' },
  { id: 4, name: 'Команда 4', captain: 'Анна Смирнова', email: 'anna@example.com', phone: '+7 999 456-78-90', caseId: 2, status: 'active' },
  { id: 5, name: 'Команда 5', captain: 'Сергей Волков', email: 'sergey@example.com', phone: '+7 999 567-89-01', caseId: 3, status: 'active' },
])

const mockInviteCodes = ref([
  { code: 'ABC123', caseId: 1, used: false, createdAt: new Date(), expiresAt: new Date(Date.now() + 7*24*60*60*1000) },
  { code: 'DEF456', caseId: 1, used: true, createdAt: new Date(), expiresAt: new Date(Date.now() + 7*24*60*60*1000) },
  { code: 'GHI789', caseId: 2, used: false, createdAt: new Date(), expiresAt: new Date(Date.now() + 7*24*60*60*1000) },
])

function loginAdmin(email, password) {
  // Демо: любой пароль работает
  if (email && password) {
    admin.value = { email, name: 'Администратор', role: 'admin' }
    localStorage.setItem('admin', JSON.stringify(admin.value))
    return true
  }
  return false
}

function send2FACode(email) {
  // Демо: отправляем код в консоль
  const code = Math.floor(100000 + Math.random() * 900000)
  console.log(`2FA Code sent to ${email}: ${code}`)
  localStorage.setItem('admin2FACode', code.toString())
  return true
}

function verify2FA(code) {
  // Для демонстрации: любой 6-значный код работает
  if (/^\d{6}$/.test(code)) {
    is2FAVerified.value = true
    localStorage.setItem('admin2FAVerified', 'true')
    return true
  }
  return false
}

function logoutAdmin() {
  admin.value = null
  is2FAVerified.value = false
  localStorage.removeItem('admin')
  localStorage.removeItem('admin2FAVerified')
  localStorage.removeItem('admin2FACode')
}

// Методы управления событиями
function createEvent(eventData) {
  return createEventStore(eventData)
}

function updateEvent(eventId, eventData) {
  return updateEventStore(eventId, eventData)
}

function deleteEvent(eventId) {
  return deleteEventStore(eventId)
}

// Методы управления кейсами
function createCase(caseData) {
  return createCaseStore(caseData)
}

function updateCase(caseId, caseData) {
  return updateCaseStore(caseId, caseData)
}

function deleteCase(caseId) {
  return deleteCaseStore(caseId)
}

// Методы управления кейсов лимитами
function updateCaseLimit(caseId, limit) {
  const caseItem = mockCases.value.find(c => c.id === caseId)
  if (caseItem) {
    caseItem.limit = limit
    return caseItem
  }
  return null
}

// Методы управления кодами приглашения
function generateInviteCode(caseId, count = 1) {
  const codes = []
  for (let i = 0; i < count; i++) {
    const code = Math.random().toString(36).substring(2, 8).toUpperCase()
    const newCode = {
      code,
      caseId,
      used: false,
      createdAt: new Date(),
      expiresAt: new Date(Date.now() + 30*24*60*60*1000), // 30 дней
    }
    mockInviteCodes.value.push(newCode)
    codes.push(code)
  }
  return codes
}

function addInviteCode(code, caseId) {
  const newCode = {
    code,
    caseId,
    used: false,
    createdAt: new Date(),
    expiresAt: new Date(Date.now() + 30*24*60*60*1000),
  }
  mockInviteCodes.value.push(newCode)
  return newCode
}

// Методы статистики
function getCaseStats(caseId) {
  const caseItem = mockCases.value.find(c => c.id === caseId)
  if (caseItem) {
    return {
      title: caseItem.title,
      limit: caseItem.limit,
      occupied: caseItem.occupied,
      available: caseItem.limit - caseItem.occupied,
      status: caseItem.status,
    }
  }
  return null
}

function getAllStats(eventId) {
  const event = mockEvents.value.find(e => e.id === eventId)
  if (!event) return null

  const cases = mockCases.value.filter(c => c.eventId === eventId)
  return {
    event: event.name,
    totalCases: cases.length,
    cases: cases.map(c => ({
      id: c.id,
      title: c.title,
      limit: c.limit,
      occupied: c.occupied,
      available: c.limit - c.occupied,
      status: c.status,
    })),
    totalTeams: mockTeams.value.filter(t => event.cases.includes(mockCases.value.find(c => c.id === t.caseId)?.id)).length,
  }
}

// Экспорт в CSV
function exportToCSV(data, filename) {
  let csv = ''
  
  if (filename.includes('stats')) {
    csv = 'Кейс,Лимит,Занято,Свободно,Статус\n'
    data.cases.forEach(c => {
      csv += `${c.title},${c.limit},${c.occupied},${c.available},${c.status}\n`
    })
  } else if (filename.includes('teams')) {
    csv = 'ID,Название,Капитан,Email,Телефон,Кейс,Статус\n'
    data.forEach(team => {
      csv += `${team.id},"${team.name}","${team.captain}",${team.email},${team.phone},${team.caseId},${team.status}\n`
    })
  }
  
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.setAttribute('href', url)
  link.setAttribute('download', filename)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

export {
  admin,
  is2FAVerified,
  mockEvents,
  mockCases,
  mockTeams,
  mockInviteCodes,
  loginAdmin,
  send2FACode,
  verify2FA,
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
  getCaseStats,
  getAllStats,
  exportToCSV,
}
