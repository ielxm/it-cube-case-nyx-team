import axios from 'axios'

// Все запросы к бэкенду будут идти на этот адрес
const api = axios.create({
  baseURL: 'http://localhost:8000',
})

export default api
