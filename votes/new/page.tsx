// 📁 app/votes/new/page.tsx

'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import axios from 'axios'
import React from 'react'

export default function CreateVotePage() {
  const router = useRouter()
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [expiresAt, setExpiresAt] = useState('')
  const [options, setOptions] = useState([''])
  const [message, setMessage] = useState('')

  const handleAddOption = () => setOptions([...options, ''])
  const handleChangeOption = (index: number, value: string) => {
    const updated = [...options]
    updated[index] = value
    setOptions(updated)
  }

  const handleSubmit = async () => {
    const payload = {
      title,
      description,
      expires_at: expiresAt,
      building: 1, // Προσωρινά static – θα γίνει dynamic βάση context
      options: options.filter(opt => opt.trim()).map(opt => ({ text: opt }))
    }

    try {
      await axios.post('/api/votes/', payload)
      setMessage('Η ψηφοφορία δημιουργήθηκε.')
      router.push('/votes')
    } catch (err) {
      console.error(err)
      setMessage('Σφάλμα κατά τη δημιουργία.')
    }
  }

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Νέα Ψηφοφορία</h1>

      <input
        type="text"
        placeholder="Τίτλος"
        value={title}
        onChange={e => setTitle(e.target.value)}
        className="w-full border px-3 py-2 rounded mb-2"
      />

      <textarea
        placeholder="Περιγραφή"
        value={description}
        onChange={e => setDescription(e.target.value)}
        className="w-full border px-3 py-2 rounded mb-2"
      />

      <input
        type="datetime-local"
        value={expiresAt}
        onChange={e => setExpiresAt(e.target.value)}
        className="w-full border px-3 py-2 rounded mb-4"
      />

      <h2 className="font-semibold mb-2">Επιλογές</h2>
      {options.map((opt, index) => (
        <input
          key={index}
          type="text"
          value={opt}
          onChange={e => handleChangeOption(index, e.target.value)}
          className="w-full border px-3 py-2 rounded mb-2"
        />
      ))}

      <button
        onClick={handleAddOption}
        className="mb-4 text-blue-600 hover:underline"
      >
        + Προσθήκη Επιλογής
      </button>

      <button
        onClick={handleSubmit}
        className="bg-blue-600 text-white px-4 py-2 rounded-xl shadow hover:bg-blue-700"
      >
        Δημιουργία Ψηφοφορίας
      </button>

      {message && <p className="mt-4 text-sm text-gray-700">{message}</p>}
    </div>
  )
}
