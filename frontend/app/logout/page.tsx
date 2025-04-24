// 📁 app/logout/page.tsx

'use client'

import { useEffect } from 'react'
import Cookies from 'js-cookie'
import { useRouter } from 'next/navigation'

export default function LogoutPage() {
  const router = useRouter()

  useEffect(() => {
    Cookies.remove('access_token')
    Cookies.remove('refresh_token')
    router.push('/login')
  }, [router])

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <p className="text-gray-500">Αποσύνδεση...</p>
    </div>
  )
}
