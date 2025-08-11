const API_BASE = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'

export async function getTask(id) {
  const res = await fetch(`${API_BASE}/tasks/${id}`, { headers: { 'x-user': localStorage.getItem('user') || 'dev@local' } })
  if (!res.ok) throw new Error('Falha ao buscar task')
  return await res.json()
}
