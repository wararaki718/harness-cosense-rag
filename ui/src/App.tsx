import { useState, useRef, useEffect } from 'react'
import { Search, Loader2, BookOpen, ExternalLink, Sparkles } from 'lucide-react'
import './App.css'

interface Context {
    title: string
    url: string
    score: number
}

interface SearchResponse {
    query: string
    answer: string
    context: Context[]
}

function App() {
    const [query, setQuery] = useState('')
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState<SearchResponse | null>(null)
    const [error, setError] = useState<string | null>(null)
    const scrollRef = useRef<HTMLDivElement>(null)

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!query.trim()) return

        setLoading(true)
        setError(null)
        setResult(null)

        try {
            const response = await fetch('http://localhost:8000/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query }),
            })

            if (!response.ok) {
                throw new Error('Search failed')
            }

            const data = await response.json()
            setResult(data)
        } catch (err) {
            setError('検索に失敗しました。サーバーが起動しているか確認してください。')
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        if (result && scrollRef.current) {
            scrollRef.current.scrollIntoView({ behavior: 'smooth' })
        }
    }, [result])

    return (
        <div className="container">
            <header>
                <div className="logo">
                    <Sparkles className="logo-icon" />
                    <h1>Cosense RAG</h1>
                </div>
                <p className="subtitle">Cosenseの知識をAIが検索・回答します</p>
            </header>

            <main>
                <form onSubmit={handleSearch} className="search-form">
                    <div className="search-input-wrapper">
                        <Search className="search-icon" />
                        <input
                            type="text"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            placeholder="知りたいことを入力してください..."
                            disabled={loading}
                            autoFocus
                        />
                        {loading ? (
                            <Loader2 className="loader-icon spin" />
                        ) : (
                            <button type="submit" disabled={!query.trim()}>
                                検索
                            </button>
                        )}
                    </div>
                </form>

                {error && <div className="error-message">{error}</div>}

                {result && (
                    <div className="result-container" ref={scrollRef}>
                        <section className="answer-section">
                            <div className="section-header">
                                <Sparkles className="section-icon" />
                                <h2>AIの回答</h2>
                            </div>
                            <div className="answer-card">
                                <p>{result.answer}</p>
                            </div>
                        </section>

                        <section className="sources-section">
                            <div className="section-header">
                                <BookOpen className="section-icon" />
                                <h2>参考ソース</h2>
                            </div>
                            <div className="sources-grid">
                                {result.context.map((ctx, idx) => (
                                    <a
                                        key={idx}
                                        href={ctx.url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="source-card"
                                    >
                                        <div className="source-info">
                                            <span className="source-title">{ctx.title}</span>
                                            <span className="source-score">関連度: {ctx.score.toFixed(2)}</span>
                                        </div>
                                        <ExternalLink className="source-link-icon" />
                                    </a>
                                ))}
                            </div>
                        </section>
                    </div>
                )}
            </main>

            <footer>
                <p>&copy; 2026 Cosense RAG System</p>
            </footer>
        </div>
    )
}

export default App
