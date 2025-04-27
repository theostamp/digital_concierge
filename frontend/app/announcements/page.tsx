// 📁 app/announcements/page.tsx

'use client'

import { useEffect, useState } from 'react'
import Cookies from 'js-cookie'
import { useRouter } from 'next/navigation'
import axios from '@/lib/axios-auth'
import { format, isSameDay } from 'date-fns'
import { el } from 'date-fns/locale'

interface Announcement {
  id: number
  title: string
  content: string
  created_at: string
  type: 'manager' | 'internal'
}

interface UserProfile {
  is_staff: boolean
  is_internal_admin: boolean
  is_tenant: boolean
}

export default function AnnouncementsPage() {
  const router = useRouter()
  const [announcements, setAnnouncements] = useState<Announcement[]>([])
  const [loading, setLoading] = useState(true)
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [type, setType] = useState<'manager' | 'internal'>('manager')
  const [submitting, setSubmitting] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [filter, setFilter] = useState<'all' | 'manager' | 'internal'>('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedDate, setSelectedDate] = useState('')
  const [user, setUser] = useState<UserProfile | null>(null)
  const [showBanner, setShowBanner] = useState(false)
  const [bannerMessage, setBannerMessage] = useState('')

  useEffect(() => {
    const token = Cookies.get('access_token')
    if (!token) {
      router.push('/login')
    } else {
      axios.get<UserProfile>('/users/me/').then(res => setUser(res.data))
      fetchAnnouncements()
    }
  }, [router])

  const fetchAnnouncements = () => {
    axios.get<Announcement[]>('/announcements/')
      .then(res => {
        setAnnouncements(res.data)
        setLoading(false)
      })
      .catch(err => {
        console.error(err)
        setLoading(false)
      })
  }

  const triggerBanner = (message: string) => {
    setBannerMessage(message)
    setShowBanner(true)
    setTimeout(() => setShowBanner(false), 4000)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    const method = editingId ? 'put' : 'post'
    const url = editingId ? `/announcements/${editingId}/` : '/announcements/'
    axios[method](url, { title, content, type })
      .then(() => {
        triggerBanner(editingId ? 'Η ανακοίνωση ενημερώθηκε.' : 'Η ανακοίνωση δημιουργήθηκε.')
        setTitle('')
        setContent('')
        setType('manager')
        setEditingId(null)
        fetchAnnouncements()
      })
      .catch(err => {
        console.error(err)
        triggerBanner('⚠️ Παρουσιάστηκε σφάλμα κατά την αποθήκευση.')
      })
      .then(
        () => setSubmitting(false),
        () => setSubmitting(false)
      )
  }

  const handleEdit = (announcement: Announcement) => {
    setTitle(announcement.title)
    setContent(announcement.content)
    setType(announcement.type)
    setEditingId(announcement.id)
  }

  const handleDelete = (id: number) => {
    if (confirm('Είστε σίγουροι ότι θέλετε να διαγράψετε την ανακοίνωση;')) {
      axios.delete(`/announcements/${id}/`)
        .then(() => {
          triggerBanner('Η ανακοίνωση διαγράφηκε.')
          fetchAnnouncements()
        })
        .catch(err => {
          console.error(err)
          triggerBanner('⚠️ Σφάλμα κατά τη διαγραφή.')
        })
    }
  }

  const filteredAnnouncements = announcements.filter(a => {
    const matchesType = filter === 'all' || a.type === filter
    const matchesSearch = a.title.toLowerCase().includes(searchTerm.toLowerCase()) || a.content.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesDate = !selectedDate || isSameDay(new Date(a.created_at), new Date(selectedDate))

    if (user?.is_staff) return matchesType && matchesSearch && matchesDate
    if (user?.is_internal_admin) return a.type === 'internal' && matchesSearch && matchesDate
    if (user?.is_tenant) return a.type === 'manager' && matchesSearch && matchesDate
    return false
  })

  const grouped = filteredAnnouncements.reduce((acc: Record<string, Announcement[]>, a) => {
    const dateKey = format(new Date(a.created_at), 'dd MMMM yyyy', { locale: el })
    acc[dateKey] = acc[dateKey] || []
    acc[dateKey].push(a)
    return acc
  }, {})

  const sortedDates = Object.keys(grouped).sort((a, b) => {
    return new Date(b).getTime() - new Date(a).getTime()
  })

  return (
    <div className="p-6 max-w-3xl mx-auto">
      {showBanner && (
        <div className="mb-4 p-3 rounded-xl bg-blue-100 border border-blue-300 text-blue-800 animate-pulse shadow text-sm text-center">
          {bannerMessage}
        </div>
      )}

      <h1 className="text-2xl font-bold text-blue-700 mb-4">Ανακοινώσεις</h1>

      {(user?.is_staff || user?.is_internal_admin) && (
        <form onSubmit={handleSubmit} className="bg-white p-4 rounded-xl shadow mb-6">
          <h2 className="text-lg font-semibold text-gray-700 mb-2">
            {editingId ? 'Επεξεργασία Ανακοίνωσης' : 'Νέα Ανακοίνωση'}
          </h2>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Τίτλος"
            className="w-full mb-2 p-2 border rounded"
            required
          />
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Περιεχόμενο"
            className="w-full mb-2 p-2 border rounded h-24"
            required
          />
          <select
            value={type}
            onChange={(e) => setType(e.target.value as 'manager' | 'internal')}
            className="w-full mb-2 p-2 border rounded"
          >
            <option value="manager">Γραφείο Διαχείρισης</option>
            <option value="internal">Εσωτερικός Διαχειριστής</option>
          </select>
          <div className="flex gap-2">
            <button
              type="submit"
              disabled={submitting}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              {editingId ? 'Αποθήκευση' : 'Δημιουργία'}
            </button>
            {!!editingId && (
              <button
                type="button"
                onClick={() => {
                  setEditingId(null)
                  setTitle('')
                  setContent('')
                  setType('manager')
                }}
                className="bg-gray-300 text-gray-700 px-4 py-2 rounded hover:bg-gray-400"
              >
                Ακύρωση
              </button>
            )}
          </div>
        </form>
      )}

      <div className="flex flex-wrap gap-4 mb-4 items-center justify-between">
        <div className="flex gap-2">
          <button onClick={() => setFilter('all')} className={`px-3 py-1 rounded ${filter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-100'}`}>Όλες</button>
          <button onClick={() => setFilter('manager')} className={`px-3 py-1 rounded ${filter === 'manager' ? 'bg-blue-600 text-white' : 'bg-gray-100'}`}>Γραφείο</button>
          <button onClick={() => setFilter('internal')} className={`px-3 py-1 rounded ${filter === 'internal' ? 'bg-blue-600 text-white' : 'bg-gray-100'}`}>Εσωτερικός</button>
        </div>
        <input
          type="date"
          value={selectedDate}
          onChange={(e) => setSelectedDate(e.target.value)}
          className="border rounded px-2 py-1 text-sm"
        />
        <input
          type="text"
          placeholder="Αναζήτηση..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="border rounded px-2 py-1 text-sm"
        />
      </div>

      {loading ? (
        <p className="text-gray-400">Φόρτωση...</p>
      ) : sortedDates.length === 0 ? (
        <p className="text-gray-500">Δεν υπάρχουν διαθέσιμες ανακοινώσεις.</p>
      ) : (
        <div className="space-y-6">
          {sortedDates.map(date => (
            <div key={date}>
              <h3 className="text-md font-semibold text-gray-600 mb-2 border-b pb-1">{date}</h3>
              <ul className="space-y-3">
                {grouped[date].map(announcement => (
                  <li key={announcement.id} className="bg-white rounded-xl shadow p-4">
                    <div className="flex justify-between items-start">
                      <div>
                        <div className="flex items-center gap-2">
                          <h2 className="text-lg font-semibold text-blue-800">{announcement.title}</h2>
                          <span className={`text-xs font-medium px-2 py-1 rounded ${announcement.type === 'manager' ? 'bg-blue-100 text-blue-700' : 'bg-green-100 text-green-700'}`}>
                            {announcement.type === 'manager' ? 'Γραφείο' : 'Εσωτερικός'}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 whitespace-pre-line mt-2">{announcement.content}</p>
                      </div>
                      {(user?.is_staff || user?.is_internal_admin) && (
                        <div className="flex flex-col gap-1 ml-4 text-sm">
                          <button onClick={() => handleEdit(announcement)} className="text-blue-600 hover:underline">Επεξεργασία</button>
                          <button onClick={() => handleDelete(announcement.id)} className="text-red-600 hover:underline">Διαγραφή</button>
                        </div>
                      )}
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
