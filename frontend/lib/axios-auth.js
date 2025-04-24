// filepath: frontend/lib/axios-auth.ts
import axios from 'axios'

const instance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/',
  // Μπορείς να προσθέσεις headers, interceptors κλπ εδώ
})

export default instance