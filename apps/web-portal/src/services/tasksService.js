const API_BASE = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'

export async function listTasks({ owner='me', skip=0, limit=50 } = {}) {
  const url = new URL(API_BASE + '/tasks')
  if (owner) url.searchParams.set('owner', owner)
  url.searchParams.set('skip', skip)
  url.searchParams.set('limit', limit)
  const res = await fetch(url, { headers: { 'x-user': localStorage.getItem('user') || 'dev@local' } })
  if (!res.ok) throw new Error('Falha ao listar tasks')
  return await res.json()
}
