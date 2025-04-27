// 📁 app/requests/page.tsx

'use client'

import { useEffect, useState } from 'react'
import Cookies from 'js-cookie'
import { useRouter } from 'next/navigation'
import axios from '@/lib/axios-auth'
import Link from 'next/link'

interface Request {
  id: number
  title: string
  description: string
  created_at: string
  status: 'pending' | 'completed'
}

interface User {
  id: number
  username: string
  is_staff: boolean
}

export default function RequestsPage() {
  const router = useRouter()
  const [requests, setRequests] = useState<Request[]>([])
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    const token = Cookies.get('access_token')
    if (!token) {
      router.push('/login')
    } else {
      fetchRequests()
      fetchUser()
    }
  }, [router])

  const fetchUser = () => {
    axios.get<User>('/users/me/')
      .then(res => setUser(res.data))
      .catch(err => console.error(err))
  }

  const fetchRequests = () => {
    axios.get<Request[]>('/requests/')
      .then(res => {
        setRequests(res.data)
        setLoading(false)
      })
      .catch(err => {
        console.error(err)
        setLoading(false)
      })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    axios.post('/requests/', { title, description })
      .then(() => {
        setTitle('')
        setDescription('')
        fetchRequests()
      })
      .catch(err => {
        console.error(err)
      })
      .then(() => setSubmitting(false))
      .catch(err => {
        console.error(err)
        setSubmitting(false)
      })
  }

  const toggleStatus = (id: number, currentStatus: 'pending' | 'completed') => {
    const newStatus = currentStatus === 'pending' ? 'completed' : 'pending'
    axios.patch(`/requests/${id}/`, { status: newStatus })
      .then(() => fetchRequests())
      .catch(err => console.error(err))
  }

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-blue-700">Αιτήματα</h1>
        {user ? (
          <div className="text-sm text-gray-600">
            Συνδεδεμένος ως: <strong>{user.username}</strong>
            {user.is_staff && <span className="ml-2 text-green-600">(Διαχειριστής)</span>}
            <Link href="/logout" className="ml-4 text-blue-600 hover:underline">Αποσύνδεση</Link>
          </div>
        ) : null}
      </div>

      <form onSubmit={handleSubmit} className="bg-white p-4 rounded-xl shadow mb-6">
        <h2 className="text-lg font-semibold text-gray-700 mb-2">Υποβολή Νέου Αιτήματος</h2>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Τίτλος"
          className="w-full mb-2 p-2 border rounded"
          required
        />
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Περιγραφή"
          className="w-full mb-2 p-2 border rounded h-24"
          required
        />
        <button
          type="submit"
          disabled={submitting}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          {submitting ? 'Αποστολή...' : 'Αποστολή'}
        </button>
      </form>

      {loading ? (
        <p className="text-gray-400">Φόρτωση...</p>
      ) : requests.length === 0 ? (
        <p className="text-gray-500">Δεν υπάρχουν καταχωρημένα αιτήματα.</p>
      ) : (
        <ul className="space-y-4">
          {requests.map((req) => (
            <li key={req.id} className="bg-white p-4 rounded-xl shadow">
              <div className="flex justify-between items-start">
                <div>
                  <h2 className="text-lg font-semibold text-blue-800">{req.title}</h2>
                  <p className="text-sm text-gray-600 whitespace-pre-line mt-2">{req.description}</p>
                  <p className="text-xs text-gray-400 mt-2">{new Date(req.created_at).toLocaleString('el-GR')}</p>
                </div>
                <div className="flex flex-col items-end gap-2">
                  <span className={`text-sm font-medium px-2 py-1 rounded ${req.status === 'completed' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'}`}>
                    {req.status === 'completed' ? 'Ολοκληρώθηκε' : 'Εκκρεμεί'}
                  </span>
                  {user?.is_staff && (
                    <button
                      onClick={() => toggleStatus(req.id, req.status)}
                      className="text-sm text-blue-600 hover:underline"
                    >
                      Αλλαγή κατάστασης
                    </button>
                  )}
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
