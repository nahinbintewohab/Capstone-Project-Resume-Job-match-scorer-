import { useState } from 'react'
import './App.css'

const API_BASE = import.meta.env.VITE_API_URL || ''

export default function App() {
  const [file, setFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    if (!file || !jobDescription.trim()) {
      setError('Please upload a resume and paste the job description.')
      return
    }
    setError('')
    setResult(null)
    setLoading(true)

    try {
      const formData = new FormData()
      formData.append('resume', file)
      formData.append('job_description', jobDescription.trim())

      const url = API_BASE ? `${API_BASE.replace(/\/$/, '')}/api/analyze` : '/api/analyze'
      const res = await fetch(url, {
        method: 'POST',
        body: formData,
      })

      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail || res.statusText || 'Analysis failed')
      }

      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError(err.message || 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Resume–Job Match Scorer</h1>
        <p>Upload your resume and paste the job description to get a match score and improvement tips.</p>
      </header>

      <form onSubmit={handleSubmit} className="form">
        <div className="field">
          <label htmlFor="resume">Resume (PDF or text)</label>
          <input
            id="resume"
            type="file"
            accept=".pdf,.txt"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
        </div>

        <div className="field">
          <label htmlFor="job">Job description</label>
          <textarea
            id="job"
            placeholder="Paste the full job description here..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            rows={8}
          />
        </div>

        {error && <p className="error">{error}</p>}

        <button type="submit" disabled={loading} className="btn">
          {loading ? 'Analyzing…' : 'Analyze match'}
        </button>
      </form>

      {result && (
        <section className="result">
          <h2>Results</h2>
          <div className="score-wrap">
            <span className="score">{result.score}</span>
            <span className="score-label">/ 100</span>
          </div>
          {result.summary && <p className="summary">{result.summary}</p>}
          {result.tips?.length > 0 && (
            <div className="tips">
              <h3>Improvement tips</h3>
              <ul>
                {result.tips.map((tip, i) => (
                  <li key={i}>{tip}</li>
                ))}
              </ul>
            </div>
          )}
        </section>
      )}
    </div>
  )
}
