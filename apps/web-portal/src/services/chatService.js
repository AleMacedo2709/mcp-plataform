const CHAT_BASE_URL = process.env.REACT_APP_CHAT_BASE_URL || 'http://localhost:8002'

export function createChatSocket() {
  const wsUrl = CHAT_BASE_URL.replace(/^http/, 'ws') + '/ws'
  const ws = new WebSocket(wsUrl)
  return ws
}

export async function chatAsk(question) {
  const res = await fetch(CHAT_BASE_URL + '/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  })
  if (!res.ok) throw new Error('Falha no chat HTTP')
  return await res.json()
}
