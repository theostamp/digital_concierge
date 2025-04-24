// 📁 app/page.tsx

'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'

interface BeforeInstallPromptEvent extends Event {
  readonly platforms: string[];
  readonly userChoice: Promise<{ outcome: 'accepted' | 'dismissed'; platform: string }>;
  prompt(): Promise<void>;
}

export default function HomePage() {
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null)
  const [showInstallButton, setShowInstallButton] = useState(false)
  const [installUnavailable, setInstallUnavailable] = useState(false)

  useEffect(() => {
    const handler = (e: Event) => {
      e.preventDefault()
      setDeferredPrompt(e as BeforeInstallPromptEvent)
      setShowInstallButton(true)
    }
    window.addEventListener('beforeinstallprompt', handler)

    const isStandalone = window.matchMedia('(display-mode: standalone)').matches || (window.navigator as any).standalone
    if (!isStandalone && !('onbeforeinstallprompt' in window)) {
      setInstallUnavailable(true)
    }

    return () => window.removeEventListener('beforeinstallprompt', handler)
  }, [])

  const handleInstall = async () => {
    if (deferredPrompt) {
      await deferredPrompt.prompt()
      const { outcome } = await deferredPrompt.userChoice
      if (outcome === 'accepted') {
        console.log('PWA installed')
        setShowInstallButton(false)
      }
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-blue-600 text-white py-6 text-center">
        <h1 className="text-4xl font-bold font-poppins">Ψηφιακός Θυρωρός</h1>
      </header>

      <main className="flex-1 bg-gray-50 py-16">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-2xl font-bold text-blue-700 mb-6">Επιλέξτε λειτουργία</h2>

          <div className="grid gap-6 md:grid-cols-3 max-w-3xl mx-auto">
            <Link href="/votes" className="block p-6 rounded-xl shadow bg-white hover:bg-blue-50">
              <h3 className="text-lg font-semibold text-blue-700 mb-2">Ψηφοφορίες</h3>
              <p className="text-sm text-gray-600">Δείτε, συμμετέχετε και δείτε τα αποτελέσματα.</p>
            </Link>
            <Link href="/announcements" className="block p-6 rounded-xl shadow bg-white hover:bg-blue-50">
              <h3 className="text-lg font-semibold text-blue-700 mb-2">Ανακοινώσεις</h3>
              <p className="text-sm text-gray-600">Ενημερωθείτε άμεσα για ό,τι αφορά την πολυκατοικία.</p>
            </Link>
            <Link href="/requests" className="block p-6 rounded-xl shadow bg-white hover:bg-blue-50">
              <h3 className="text-lg font-semibold text-blue-700 mb-2">Αιτήματα</h3>
              <p className="text-sm text-gray-600">Υποβάλετε ή παρακολουθήστε την εξέλιξη αιτημάτων.</p>
            </Link>
          </div>

          {showInstallButton && (
            <button
              onClick={handleInstall}
              className="mt-8 px-6 py-2 rounded-md text-sm font-semibold bg-blue-700 hover:bg-blue-800 text-white"
            >
              Εγκατάσταση Εφαρμογής
            </button>
          )}

          {installUnavailable && (
            <p className="mt-4 text-sm text-gray-500">Η εγκατάσταση υποστηρίζεται μόνο σε Android ή Chrome περιβάλλον.</p>
          )}
        </div>
      </main>

      <footer className="bg-gray-100 py-6 text-center text-gray-600 text-sm border-t">
        <div className="container mx-auto px-6">
          <div className="mb-2">
            <button className="mx-2 hover:underline text-blue-600 bg-transparent border-none cursor-pointer">Όροι Χρήσης</button>
            <button className="mx-2 hover:underline text-blue-600 bg-transparent border-none cursor-pointer">Πολιτική Απορρήτου</button>
            <button className="mx-2 hover:underline text-blue-600 bg-transparent border-none cursor-pointer">Επικοινωνία</button>
          </div>
          <div>&copy; 2025 Ψηφιακός Θυρωρός. All Rights Reserved.</div>
        </div>
      </footer>
    </div>
  )
}
