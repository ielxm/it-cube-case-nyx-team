import { ref } from 'vue'
import api from '../api.js'

const events = ref([])
const cases  = ref([])

async function fetchAll() {
  const [evRes, caseRes] = await Promise.all([
    api.get('/admin/events'),
    api.get('/admin/cases'),
  ])
  events.value = evRes.data
  cases.value  = caseRes.data
}

async function createEvent(data) {
  const res = await api.post('/events', data)
  await fetchAll()
  return res.data
}

async function updateEvent(id, data) {
  await api.put(`/events/${id}`, data)
  await fetchAll()
}

async function deleteEvent(id) {
  await api.delete(`/events/${id}`)
  events.value = events.value.filter(e => e.id !== id)
}

async function createCase(data) {
  const res = await api.post('/cases', data)
  await fetchAll()
  return res.data
}

async function updateCase(id, data) {
  await api.put(`/cases/${id}`, data)
  await fetchAll()
}

async function deleteCase(id) {
  await api.delete(`/cases/${id}`)
  cases.value = cases.value.filter(c => c.id !== id)
}

function getEventBySlug(slug) {
  return events.value.find(e => e.slug === slug)
}

function getCasesByEventId(eventId) {
  return cases.value.filter(c => c.event_id === eventId)
}

export {
  events, cases, fetchAll,
  createEvent, updateEvent, deleteEvent,
  createCase, updateCase, deleteCase,
  getEventBySlug, getCasesByEventId,
}
