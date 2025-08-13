const CHAT_BASE_URL = (import.meta?.env?.VITE_CHAT_BASE_URL || process.env.REACT_APP_CHAT_BASE_URL || 'http://localhost:8002')

export function createChatSocket(token) {
  const base = CHAT_BASE_URL.replace(/^http/, 'ws')
  const wsUrl = token ? `${base}/ws?token=${encodeURIComponent(token)}` : `${base}/ws`
  const ws = new WebSocket(wsUrl)
  return ws
}

export async function chatAsk(question, { timeoutMs = 10000, retries = 1, token } = {}) {
  const controller = new AbortController()
  const t = setTimeout(() => controller.abort(), timeoutMs)
  try {
    const res = await fetch(CHAT_BASE_URL + '/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}) },
      body: JSON.stringify({ question }),
      signal: controller.signal
    })
    if (!res.ok) throw new Error('Falha no chat HTTP')
    return await res.json()
  } catch (e) {
    if (retries > 0) {
      await new Promise(r => setTimeout(r, 500))
      return chatAsk(question, { timeoutMs: Math.min(timeoutMs * 1.5, 20000), retries: retries - 1 })
    }
    throw e
  } finally {
    clearTimeout(t)
  }
}
