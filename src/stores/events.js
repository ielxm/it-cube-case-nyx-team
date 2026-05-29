import { ref } from 'vue'

// Глобальный store мероприятий
const events = ref([
  {
    id: 1,
    name: 'IT Cube Case 2024',
    slug: 'it-cube-2024',
    title: 'IT Cube Case 2024',
    description: 'Первый чемпионат IT Cube',
    cases: [1, 2, 3],
    status: 'active',
    createdAt: new Date('2024-01-01'),
  }
])

const cases = ref([
  { id: 1, title: 'Кейс 1', eventId: 1, description: 'Описание кейса 1', limit: 5, occupied: 3, status: 'active' },
  { id: 2, title: 'Кейс 2', eventId: 1, description: 'Описание кейса 2', limit: 5, occupied: 4, status: 'active' },
  { id: 3, title: 'Кейс 3', eventId: 1, description: 'Описание кейса 3', limit: 5, occupied: 2, status: 'active' },
])

// Методы управления событиями
function createEvent(eventData) {
  const newEvent = {
    id: Math.max(...events.value.map(e => e.id), 0) + 1,
    name: eventData.name,
    title: eventData.name,
    slug: eventData.slug,
    description: eventData.description,
    cases: [],
    status: eventData.status || 'draft',
    createdAt: new Date(),
  }
  events.value.push(newEvent)
  return newEvent
}

function updateEvent(eventId, eventData) {
  const event = events.value.find(e => e.id === eventId)
  if (event) {
    if (eventData.name) event.name = eventData.name
    if (eventData.title) event.title = eventData.name
    if (eventData.slug) event.slug = eventData.slug
    if (eventData.description) event.description = eventData.description
    if (eventData.status) event.status = eventData.status
    return event
  }
  return null
}

function deleteEvent(eventId) {
  const index = events.value.findIndex(e => e.id === eventId)
  if (index > -1) {
    events.value.splice(index, 1)
    return true
  }
  return false
}

function getEventBySlug(slug) {
  return events.value.find(e => e.slug === slug)
}

function createCase(caseData) {
  const newCase = {
    id: Math.max(...cases.value.map(c => c.id), 0) + 1,
    ...caseData,
    occupied: 0,
    status: 'active',
  }
  cases.value.push(newCase)
  if (caseData.eventId) {
    const event = events.value.find(e => e.id === caseData.eventId)
    if (event && !event.cases.includes(newCase.id)) {
      event.cases.push(newCase.id)
    }
  }
  return newCase
}

function updateCase(caseId, caseData) {
  const caseItem = cases.value.find(c => c.id === caseId)
  if (caseItem) {
    Object.assign(caseItem, caseData)
    return caseItem
  }
  return null
}

function deleteCase(caseId) {
  const index = cases.value.findIndex(c => c.id === caseId)
  if (index > -1) {
    cases.value.splice(index, 1)
    return true
  }
  return false
}

function getCasesByEventId(eventId) {
  return cases.value.filter(c => c.eventId === eventId)
}

export {
  events,
  cases,
  createEvent,
  updateEvent,
  deleteEvent,
  getEventBySlug,
  createCase,
  updateCase,
  deleteCase,
  getCasesByEventId,
}
