// 📄 frontend/app/layout.tsx

import React from "react"

export const metadata = {
    title: 'Ψηφιακός Θυρωρός',
    description: 'PWA πλατφόρμα διαχείρισης πολυκατοικίας'
  }
  
  export default function RootLayout({ children }: { readonly children: React.ReactNode }) {
    return (
      <html lang="el">
        <head>
          <link rel="manifest" href="/manifest.json" />
          <link rel="apple-touch-icon" href="/icons/icon-192.png" />
          <meta name="theme-color" content="#2563eb" />
        </head>
        <body>{children}</body>
      </html>
    )
  }
  