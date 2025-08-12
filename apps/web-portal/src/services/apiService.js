import axios from 'axios'

export const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:18000'
export const INGESTION_BASE_URL = process.env.REACT_APP_INGESTION_BASE_URL || 'http://localhost:18001'

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
  const res = await axios.post(`${API_BASE_URL}/projects`, payload, { headers: { 'x-role': 'editor', 'x-user': 'tester@local' } })
  return res.data
}

export async function getProject(id) {
  const res = await axios.get(`${API_BASE_URL}/projects/${id}`)
  return res.data
}

export async function updateProject(id, payload) {
  const res = await axios.put(`${API_BASE_URL}/projects/${id}`, payload, { headers: { 'x-role': 'editor', 'x-user': 'tester@local' } })
  return res.data
}

// deleteProject removido em favor de projectService.delete

export const projectService = {
  headers(role='editor', user='tester@local') { return { 'x-role': role, 'x-user': user } },
  async getAll(params = {}) {
    // Pass-through for existing components expecting getAll with skip/limit/search/filters
    const query = new URLSearchParams()
    for (const [k, v] of Object.entries(params)) {
      if (v !== undefined && v !== null && v !== '') query.set(k, String(v))
    }
    const res = await axios.get(`${API_BASE_URL}/projects?${query.toString()}`)
    return res.data // { projects, total }
  },
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
  },
  async delete(id) {
    const res = await axios.delete(`${API_BASE_URL}/projects/${id}`, { headers: this.headers('admin') })
    return res.data
  }
}

export async function uploadProjectAttachment(projectId, file) {
  const form = new FormData()
  form.append('file', file)
  const res = await axios.post(`${API_BASE_URL}/projects/${projectId}/attachments`, form, { headers: { 'Content-Type': 'multipart/form-data', ...projectService.headers('editor') } })
  return res.data
}

export async function uploadProjectCover(projectId, file) {
  const form = new FormData()
  form.append('file', file)
  const res = await axios.post(`${API_BASE_URL}/projects/${projectId}/cover`, form, { headers: { 'Content-Type': 'multipart/form-data', ...projectService.headers('editor') } })
  return res.data
}

export async function listProjectAttachments(projectId) {
  const res = await axios.get(`${API_BASE_URL}/projects/${projectId}/attachments`)
  return res.data
}

export const reportService = {
  async dashboard() {
    const res = await axios.get(`${API_BASE_URL}/reports/dashboard`, { headers: { 'x-origin': 'web-portal' } })
    return res.data
  }
}
