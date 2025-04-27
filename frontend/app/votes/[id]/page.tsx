// 📁 app/votes/[id]/page.tsx

'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import axios from 'axios'

interface VoteOption {
  id: number
  text: string
  votes_count?: number
  percentage?: number
}

interface VoteDetail {
  id: number
  title: string
  description: string
  expires_at: string
  options: VoteOption[]
  has_voted?: boolean
  voted_option_id?: number
}

export default function VoteDetailPage() {
  const { id } = useParams()
  const [vote, setVote] = useState<VoteDetail | null>(null)
  const [selectedOption, setSelectedOption] = useState<number | null>(null)
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(true)
  const [hasVoted, setHasVoted] = useState(false)
  const [votedOptionId, setVotedOptionId] = useState<number | null>(null)

  useEffect(() => {
    axios.get<VoteDetail>(`/api/votes/${id}/`).then(res => {
      setVote(res.data)
      setHasVoted(res.data.has_voted ?? false)
      setVotedOptionId(res.data.voted_option_id || null)
    })
    .catch(err => setMessage('Σφάλμα φόρτωσης'))
    .then(() => setLoading(false), () => setLoading(false))
  }, [id])

  const handleVote = () => {
    if (!selectedOption) return setMessage('Επιλέξτε μία επιλογή')

    axios.post(`/api/votes/${id}/vote/`, { option: selectedOption })
      .then(() => {
        setMessage('Η ψήφος σας καταχωρήθηκε')
        setHasVoted(true)
        setVotedOptionId(selectedOption)
        fetchResults()
      })
      .catch(() => setMessage('Έχετε ήδη ψηφίσει ή προέκυψε σφάλμα'))
  }

  const fetchResults = () => {
    axios.get<{ results: VoteOption[] }>(`/api/votes/${id}/results/`).then(res => {
      setVote(prev => prev ? { ...prev, options: res.data.results } : null)
    })
  }

  if (loading) return <p className="p-4">Φόρτωση...</p>
  if (!vote) return <p className="p-4 text-red-500">{message}</p>

  const isExpired = new Date(vote.expires_at) < new Date()

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <div className="flex justify-between items-center mb-2">
        <h1 className="text-2xl font-bold">{vote.title}</h1>
        {hasVoted && (
          <span className="text-sm text-green-600 font-medium bg-green-100 px-2 py-1 rounded">Ψηφίσατε</span>
        )}
      </div>
      <p className="mb-4 text-gray-600">{vote.description}</p>
      {isExpired || hasVoted ? (
        <div className="space-y-2">
          <p className="text-blue-700 font-medium mb-2">
            {isExpired ? 'Η ψηφοφορία έχει λήξει. Αποτελέσματα:' : 'Έχετε ήδη ψηφίσει. Δείτε τα αποτελέσματα:'}
          </p>
          {vote.options.map(option => (
            <div key={option.id} className="mb-2">
              <div className="flex justify-between text-sm">
                <span>
                  {option.text}
                  {option.id === votedOptionId && (
                    <span className="ml-2 text-green-600 font-medium">(Η επιλογή σας)</span>
                  )}
                </span>
                <span>{option.percentage?.toFixed(1)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-4">
                <div
                  className="bg-blue-600 h-4 rounded-full"
                  style={{ width: `${option.percentage || 0}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="space-y-2">
          {vote.options.map(option => (
            <div key={option.id} className="flex items-center gap-2">
              <input
                type="radio"
                name="voteOption"
                value={option.id}
                onChange={() => setSelectedOption(option.id)}
              />
              <label>{option.text}</label>
            </div>
          ))}
          <button
            onClick={handleVote}
            className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-xl shadow hover:bg-blue-700"
          >
            Υποβολή Ψήφου
          </button>
        </div>
      )}
      {message && <p className="mt-4 text-sm text-gray-700">{message}</p>}
    </div>
  )
}