import { useState } from 'react'
import './App.css'
import { supabase } from './supabaseClient'

function App() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [user, setUser] = useState(null)
  const [symbol, setSymbol] = useState('')
  const [price, setPrice] = useState(null)

  const signIn = async () => {
    const { data, error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) {
      alert(error.message)
    } else {
      setUser(data.user)
    }
  }

  const fetchPrice = async () => {
    if (!symbol) return
    const token = (await supabase.auth.getSession()).data.session?.access_token
    const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/stock/${symbol}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {}
    })
    if (!res.ok) {
      alert('Error fetching price')
      return
    }
    const json = await res.json()
    setPrice(json.price)
  }

  return (
    <div className="App">
      {!user && (
        <div className="login">
          <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
          <input placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
          <button onClick={signIn}>Sign In</button>
        </div>
      )}
      {user && (
        <div className="trade">
          <p>Signed in as {user.email}</p>
          <input placeholder="Symbol" value={symbol} onChange={e => setSymbol(e.target.value)} />
          <button onClick={fetchPrice}>Get Price</button>
          {price && <p>Price: {price}</p>}
        </div>
      )}
    </div>
  )
}

export default App
