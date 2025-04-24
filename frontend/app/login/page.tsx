'use client'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const router = useRouter()

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [csrfToken, setCsrfToken] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  // Ελέγχει αν είναι ήδη logged in (π.χ. από localStorage)
  useEffect(() => {
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
    if (isLoggedIn) {
      router.push('/dashboard') // ή όπου θέλεις
    }
  }, [router])

  // Φέρνει CSRF token
  useEffect(() => {
    fetch('http://localhost:8000/api/auth/login/', {
      method: 'GET',
      credentials: 'include',
    }).then(res => {
      const token = res.headers.get('X-CSRFToken')
      if (token) setCsrfToken(token)
    })
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    const response = await fetch('http://localhost:8000/api/auth/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrfToken,
      },
      credentials: 'include',
      body: new URLSearchParams({
        username,
        password,
      }),
    })

    setLoading(false)

    if (response.ok) {
      localStorage.setItem('isLoggedIn', 'true')
      router.push('/dashboard')
    } else {
      setError('Λάθος στοιχεία. Δοκιμάστε ξανά.')
    }
  }

  return (
    <div className="max-w-sm mx-auto mt-20">
      <h1 className="text-2xl font-semibold mb-4">Σύνδεση</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          placeholder="Όνομα χρήστη"
          value={username}
          onChange={e => setUsername(e.target.value)}
          className="w-full p-2 border rounded"
        />
        <input
          type="password"
          placeholder="Κωδικός"
          value={password}
          onChange={e => setPassword(e.target.value)}
          className="w-full p-2 border rounded"
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          {loading ? 'Γίνεται σύνδεση...' : 'Σύνδεση'}
        </button>
      </form>
      {error && <p className="text-red-500 mt-3">{error}</p>}
    </div>
  )
}
