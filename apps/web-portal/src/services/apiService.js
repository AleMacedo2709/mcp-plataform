import axios from 'axios'

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'
const INGESTION_BASE_URL = process.env.REACT_APP_INGESTION_BASE_URL || 'http://localhost:8001'

// ---- Upload & IA ----
export async function uploadDocument(file, analysisType = 'analyze_project_document_cnmp') {
  const form = new FormData()
  form.append('file', file)
  const url = `${INGESTION_BASE_URL}/analyze?analysis_type=${encodeURIComponent(analysisType)}`
  const res = await axios.post(url, form, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  return res.data // { analysis: {...} }
}

// ---- Projetos (CRUD) ----
export async function createProject(payload) {
  const res = await axios.post(`${API_BASE_URL}/projects`, payload)
  return res.data
}

export async function getProject(id) {
  const res = await axios.get(`${API_BASE_URL}/projects/${id}`)
  return res.data
}

export async function updateProject(id, payload) {
  const res = await axios.put(`${API_BASE_URL}/projects/${id}`, payload)
  return res.data
}

export async function deleteProject(id) {
  const res = await axios.delete(`${API_BASE_URL}/projects/${id}`)
  return res.data
}

export const projectService = {
  async list({ page = 1, limit = 10, search = '', tipo_iniciativa = '', classificacao = '', fase = '', orderBy = 'created_at', order = 'desc' } = {}) {
    const params = new URLSearchParams()
    params.set('skip', String((page - 1) * limit))
    params.set('limit', String(limit))
    if (search) params.set('search', search)
    if (tipo_iniciativa) params.set('tipo_iniciativa', tipo_iniciativa)
    if (classificacao) params.set('classificacao', classificacao)
    if (fase) params.set('fase', fase)
    if (orderBy) params.set('orderBy', orderBy)
    if (order) params.set('order', order)

    const res = await axios.get(`${API_BASE_URL}/projects?${params.toString()}`)
    return res.data // { projects, total }
  }
}

export const reportService = {
  async dashboard() {
    const res = await axios.get(`${API_BASE_URL}/reports/dashboard`)
    return res.data
  }
}
