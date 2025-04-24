// 📁 app/votes/page.tsx

'use client'

import React, { useEffect, useState } from 'react'
import axios from 'axios'
import Link from 'next/link'
// fallback icon
import { ChevronRightIcon } from '@heroicons/react/24/solid'

interface Vote {
  id: number
  title: string
  expires_at: string
  created_at: string
  has_voted?: boolean
}

export default function VotesPage() {
  const [votes, setVotes] = useState<Vote[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | 'active' | 'voted' | 'expired'>('all')

  useEffect(() => {
    axios.get<Vote[]>('/api/votes/')
      .then(res => {
        const sortedVotes = res.data.toSorted((a, b) => new Date(a.expires_at).getTime() - new Date(b.expires_at).getTime())
        setVotes(sortedVotes)
        setLoading(false)
      })
      .catch(err => {
        console.error(err)
        setLoading(false)
      })
  }, [])

  const filteredVotes = votes.filter(vote => {
    const now = new Date()
    const isExpired = new Date(vote.expires_at) < now
    if (filter === 'active') return !isExpired
    if (filter === 'expired') return isExpired
    if (filter === 'voted') return vote.has_voted
    return true
  })

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:justify-between items-start sm:items-center mb-6">
        <h1 className="text-3xl font-bold text-blue-700 mb-2 sm:mb-0">Ψηφοφορίες</h1>
        <div className="flex gap-2">
          <button onClick={() => setFilter('all')} className={`px-3 py-1 rounded-xl ${filter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-100'}`}>Όλες</button>
          <button onClick={() => setFilter('active')} className={`px-3 py-1 rounded-xl ${filter === 'active' ? 'bg-blue-600 text-white' : 'bg-gray-100'}`}>Ενεργές</button>
          <button onClick={() => setFilter('voted')} className={`px-3 py-1 rounded-xl ${filter === 'voted' ? 'bg-blue-600 text-white' : 'bg-gray-100'}`}>Ψηφισμένες</button>
          <button onClick={() => setFilter('expired')} className={`px-3 py-1 rounded-xl ${filter === 'expired' ? 'bg-blue-600 text-white' : 'bg-gray-100'}`}>Ληγμένες</button>
        </div>
      </div>

      {(() => {
        if (loading) {
          return <p className="animate-pulse text-gray-400">Φόρτωση...</p>
        }

        if (filteredVotes.length === 0) {
          return <p className="text-gray-500">Δεν υπάρχουν ψηφοφορίες σε αυτήν την κατηγορία.</p>
        }

        return (
          <div className="grid gap-4">
            {filteredVotes.map(vote => {
              const isExpired = new Date(vote.expires_at) < new Date()
              return (
                <Link key={vote.id} href={`/votes/${vote.id}`} className="block">
                  <div className="rounded-2xl p-4 shadow bg-white hover:bg-gray-50 transition">
                    <div className="flex justify-between items-center">
                      <h2 className="text-lg font-semibold text-blue-800">{vote.title}</h2>
                      {vote.has_voted && (
                        <span className="text-sm text-green-600 font-medium bg-green-100 px-2 py-1 rounded">Ψηφίσατε</span>
                      )}
                    </div>
                    <div className="flex justify-between items-end mt-2 text-sm">
                      <p className={isExpired ? 'text-red-500' : 'text-gray-500'}>
                        Έως: {new Date(vote.expires_at).toLocaleDateString('el-GR')}
                        {isExpired && ' (Έληξε)'}
                      </p>
                      <ChevronRightIcon className="w-4 h-4 text-gray-400" />
                    </div>
                  </div>
                </Link>
              )
            })}
          </div>
        )
      })()}
    </div>
  )
}
