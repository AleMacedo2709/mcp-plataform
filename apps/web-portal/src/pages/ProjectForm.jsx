import React, { useEffect, useState } from 'react'
import { useLocation, useParams, useNavigate } from 'react-router-dom'
import { Container, Paper, Typography, Box, Button, TextField, Grid, Alert, FormControl, InputLabel, Select, MenuItem, Divider, IconButton, Stack } from '@mui/material'
import { Add, Delete } from '@mui/icons-material'
import { ArrowBack, Save } from '@mui/icons-material'
import { getProject, updateProject, createProject, uploadProjectCover, uploadProjectAttachment, API_BASE_URL, projectService } from '../services/apiService'
import LoadingSpinner from '../components/LoadingSpinner'
import { toast } from 'react-toastify'
import { tipoOptions, classificacaoOptions, faseOptions } from '../constants/formOptions'

const ProjectForm = () => {
  const location = useLocation()
  const navigate = useNavigate()
  const { id } = useParams()
  const isEdit = Boolean(id)
  const prefill = (location?.state && location.state.prefill) || null
  
  const [formData, setFormData] = useState({
    // 29 campos baseados no backend
    owner: '',
    nome_da_iniciativa: '',
    tipo_de_iniciativa: '',
    classificacao: '',
    natureza_da_iniciativa: '',
    iniciativa_vinculada: '',
    objetivo_estrategico_pen_mp: '',
    programa_pen_mp: '',
    promocao_do_objetivo_estrategico: '',
    data_inicial_de_operacao: '',
    fase_de_implementacao: '',
    descricao: '',
    estimativa_de_recursos: '',
    publico_impactado: '',
    orgaos_envolvidos: '',
    contatos: '',
    desafio_1: '',
    desafio_2: '',
    desafio_3: '',
    resolutividade: '',
    inovacao: '',
    transparencia: '',
    proatividade: '',
    cooperacao: '',
    resultado_1: '',
    resultado_2: '',
    resultado_3: '',
    comprovacao_dos_resultados: '',
    capa_da_iniciativa: '',
    categoria: ''
  })
  const [coverFile, setCoverFile] = useState(null)
  const [attachmentFiles, setAttachmentFiles] = useState([])
  const [members, setMembers] = useState([{ name:'', email:'', role:'' }])
  const [loading, setLoading] = useState(isEdit)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)

  const limits = {
    owner: 320,
    nome_da_iniciativa: 300,
    tipo_de_iniciativa: 300,
    classificacao: 300,
    natureza_da_iniciativa: 100,
    iniciativa_vinculada: 300,
    objetivo_estrategico_pen_mp: 300,
    programa_pen_mp: 300,
    promocao_do_objetivo_estrategico: 100,
    data_inicial_de_operacao: 300,
    fase_de_implementacao: 300,
    descricao: 1000,
    estimativa_de_recursos: 200,
    publico_impactado: 100,
    orgaos_envolvidos: 300,
    contatos: 300,
    desafio_1: 100,
    desafio_2: 100,
    desafio_3: 100,
    resolutividade: 500,
    inovacao: 500,
    transparencia: 500,
    proatividade: 500,
    cooperacao: 500,
    resultado_1: 100,
    resultado_2: 100,
    resultado_3: 100,
    comprovacao_dos_resultados: 300,
    capa_da_iniciativa: 300,
    categoria: 300,
  }

  const limitProps = (field) => {
    const max = limits[field]
    if (!max) return {}
    const value = formData[field] || ''
    return {
      inputProps: { maxLength: max },
      helperText: `${value.length}/${max}`
    }
  }

  useEffect(() => {
    if (!isEdit && prefill) {
      setFormData((prev) => ({ ...prev, ...prefill }))
    }
  }, [isEdit, prefill])

  useEffect(() => {
    if (!isEdit || !id) return
    const fetchProject = async () => {
      try {
        setLoading(true)
        const data = await getProject(id)
        setFormData({
          owner: data.owner || '',
          nome_da_iniciativa: data.nome_da_iniciativa || data.nome_iniciativa || '',
          tipo_de_iniciativa: data.tipo_de_iniciativa || data.tipo_iniciativa || '',
          classificacao: data.classificacao || '',
          natureza_da_iniciativa: data.natureza_da_iniciativa || '',
          iniciativa_vinculada: data.iniciativa_vinculada || '',
          objetivo_estrategico_pen_mp: data.objetivo_estrategico_pen_mp || '',
          programa_pen_mp: data.programa_pen_mp || '',
          promocao_do_objetivo_estrategico: data.promocao_do_objetivo_estrategico || '',
          data_inicial_de_operacao: data.data_inicial_de_operacao || data.data_inicial_operacao || '',
          fase_de_implementacao: data.fase_de_implementacao || data.fase_implementacao || data.fase || '',
          descricao: data.descricao || '',
          estimativa_de_recursos: data.estimativa_de_recursos || '',
          publico_impactado: data.publico_impactado || '',
          orgaos_envolvidos: data.orgaos_envolvidos || '',
          contatos: data.contatos || '',
          desafio_1: data.desafio_1 || '',
          desafio_2: data.desafio_2 || '',
          desafio_3: data.desafio_3 || '',
          resolutividade: data.resolutividade || '',
          inovacao: data.inovacao || '',
          transparencia: data.transparencia || '',
          proatividade: data.proatividade || '',
          cooperacao: data.cooperacao || '',
          resultado_1: data.resultado_1 || '',
          resultado_2: data.resultado_2 || '',
          resultado_3: data.resultado_3 || '',
          comprovacao_dos_resultados: data.comprovacao_dos_resultados || '',
          capa_da_iniciativa: data.capa_da_iniciativa || '',
          categoria: data.categoria || ''
        })
      } catch (err) {
        setError('Erro ao carregar projeto')
        console.error('Erro ao buscar projeto:', err)
      } finally {
        setLoading(false)
      }
    }
    fetchProject()
  }, [isEdit, id])

  const handleChange = (field) => (event) => {
    setFormData((prev) => ({ ...prev, [field]: event.target.value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (!formData.nome_da_iniciativa.trim()) {
      toast.error('Nome da iniciativa é obrigatório')
      return
    }
    if (!formData.descricao.trim()) {
      toast.error('Descrição é obrigatória')
      return
    }
    try {
      setSaving(true)
      if (isEdit) {
        const saved = await updateProject(id, formData)
        // Sync members (simple replace approach)
        if (Array.isArray(members)) {
          for (const m of members) {
            if (!m || !m.name || !m.email) continue
            await fetch(`${API_BASE_URL}/projects/${saved.id || id}/members`, {
              method:'POST', headers:{ 'Content-Type':'application/json', ...projectService.headers('editor') }, body:JSON.stringify(m)
            })
          }
        }
        if (coverFile) { await uploadProjectCover(saved.id || id, coverFile) }
        if (attachmentFiles && attachmentFiles.length) {
          for (const f of attachmentFiles) { await uploadProjectAttachment(saved.id || id, f) }
        }
        toast.success('Projeto atualizado com sucesso!')
      } else {
        const created = await createProject(formData)
        if (Array.isArray(members)) {
          for (const m of members) {
            if (!m || !m.name || !m.email) continue
            await fetch(`${API_BASE_URL}/projects/${created.id}/members`, {
              method:'POST', headers:{ 'Content-Type':'application/json', ...projectService.headers('editor') }, body:JSON.stringify(m)
            })
          }
        }
        if (coverFile) { await uploadProjectCover(created.id, coverFile) }
        if (attachmentFiles && attachmentFiles.length) {
          for (const f of attachmentFiles) { await uploadProjectAttachment(created.id, f) }
        }
        toast.success('Projeto criado com sucesso!')
      }
      navigate('/projects')
    } catch (err) {
      toast.error(isEdit ? 'Erro ao atualizar projeto' : 'Erro ao criar projeto')
      console.error('Erro ao salvar projeto:', err)
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <LoadingSpinner message="Carregando projeto..." />
  if (error) return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Alert severity="error">{error}</Alert>
      <Box sx={{ mt: 2 }}>
        <Button variant="outlined" startIcon={<ArrowBack />} onClick={() => navigate('/projects')}>
            Voltar para Projetos
          </Button>
        </Box>
      </Container>
  )

  return (
    <Container maxWidth={false} sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 1 }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 800 }}>{isEdit ? '✏️ Editar Projeto' : '➕ Novo Projeto'}</Typography>
        <Button variant="outlined" startIcon={<ArrowBack />} onClick={() => navigate('/projects')} disabled={saving}>
          Voltar
        </Button>
      </Box>

      <Paper sx={{ p: { xs: 2, md: 4 } }}>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={{ xs: 2, md: 3 }}>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom sx={{ color: 'primary.main', fontWeight: 'bold' }}>
                📋 1. Identificação da Iniciativa
              </Typography>
              <Divider sx={{ mb: 2, borderColor: 'rgba(0,0,0,0.08)' }} />
            </Grid>

            <Grid item xs={12}>
              <TextField fullWidth label="Nome da Iniciativa *" value={formData.nome_da_iniciativa} onChange={handleChange('nome_da_iniciativa')} required {...limitProps('nome_da_iniciativa')} />
            </Grid>

            <Grid item xs={12} md={4}>
              <FormControl fullWidth required>
                <InputLabel>Tipo de Iniciativa *</InputLabel>
                <Select value={formData.tipo_de_iniciativa} onChange={handleChange('tipo_de_iniciativa')} label="Tipo de Iniciativa *">
                  {tipoOptions.map((tipo) => (<MenuItem key={tipo} value={tipo}>{tipo}</MenuItem>))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} md={4}>
              <FormControl fullWidth required>
                <InputLabel>Classificação *</InputLabel>
                <Select value={formData.classificacao} onChange={handleChange('classificacao')} label="Classificação *">
                  {classificacaoOptions.map((c) => (<MenuItem key={c} value={c}>{c}</MenuItem>))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>Fase de Implementação</InputLabel>
                <Select value={formData.fase_de_implementacao} onChange={handleChange('fase_de_implementacao')} label="Fase de Implementação">
                  {faseOptions.map((f) => (<MenuItem key={f} value={f}>{f}</MenuItem>))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField fullWidth label="Data Inicial de Operação" value={formData.data_inicial_de_operacao} onChange={handleChange('data_inicial_de_operacao')} type="date" InputLabelProps={{ shrink: true }} {...limitProps('data_inicial_de_operacao')} />
            </Grid>

            <Grid item xs={12}>
              <TextField fullWidth multiline rows={5} label="Descrição *" value={formData.descricao} onChange={handleChange('descricao')} required {...limitProps('descricao')} />
            </Grid>

            {/* Campos adicionais */}
            <Grid item xs={12} md={6}><TextField fullWidth label="Natureza da Iniciativa" value={formData.natureza_da_iniciativa} onChange={handleChange('natureza_da_iniciativa')} {...limitProps('natureza_da_iniciativa')} /></Grid>
            <Grid item xs={12} md={6}><TextField fullWidth label="Iniciativa Vinculada" value={formData.iniciativa_vinculada} onChange={handleChange('iniciativa_vinculada')} {...limitProps('iniciativa_vinculada')} /></Grid>
            <Grid item xs={12} md={6}><TextField fullWidth label="Objetivo Estratégico PEN-MP" value={formData.objetivo_estrategico_pen_mp} onChange={handleChange('objetivo_estrategico_pen_mp')} {...limitProps('objetivo_estrategico_pen_mp')} /></Grid>
            <Grid item xs={12} md={6}><TextField fullWidth label="Programa PEN-MP" value={formData.programa_pen_mp} onChange={handleChange('programa_pen_mp')} {...limitProps('programa_pen_mp')} /></Grid>
            <Grid item xs={12} md={6}><TextField fullWidth label="Promoção do Objetivo Estratégico" value={formData.promocao_do_objetivo_estrategico} onChange={handleChange('promocao_do_objetivo_estrategico')} {...limitProps('promocao_do_objetivo_estrategico')} /></Grid>
            <Grid item xs={12} md={6}><TextField fullWidth label="Estimativa de Recursos" value={formData.estimativa_de_recursos} onChange={handleChange('estimativa_de_recursos')} {...limitProps('estimativa_de_recursos')} /></Grid>
            <Grid item xs={12} md={6}><TextField fullWidth label="Público Impactado" value={formData.publico_impactado} onChange={handleChange('publico_impactado')} {...limitProps('publico_impactado')} /></Grid>
            <Grid item xs={12} md={6}><TextField fullWidth label="Órgãos Envolvidos" value={formData.orgaos_envolvidos} onChange={handleChange('orgaos_envolvidos')} {...limitProps('orgaos_envolvidos')} /></Grid>
            <Grid item xs={12} md={6}><TextField fullWidth label="Contatos" value={formData.contatos} onChange={handleChange('contatos')} {...limitProps('contatos')} /></Grid>
            <Grid item xs={12} md={4}><TextField fullWidth label="Desafio 1" value={formData.desafio_1} onChange={handleChange('desafio_1')} {...limitProps('desafio_1')} /></Grid>
            <Grid item xs={12} md={4}><TextField fullWidth label="Desafio 2" value={formData.desafio_2} onChange={handleChange('desafio_2')} {...limitProps('desafio_2')} /></Grid>
            <Grid item xs={12} md={4}><TextField fullWidth label="Desafio 3" value={formData.desafio_3} onChange={handleChange('desafio_3')} {...limitProps('desafio_3')} /></Grid>
            <Grid item xs={12} md={6}><TextField fullWidth label="Resolutividade" value={formData.resolutividade} onChange={handleChange('resolutividade')} {...limitProps('resolutividade')} /></Grid>
            <Grid item xs={12} md={6}><TextField fullWidth label="Inovação" value={formData.inovacao} onChange={handleChange('inovacao')} {...limitProps('inovacao')} /></Grid>
            <Grid item xs={12} md={6}><TextField fullWidth label="Transparência" value={formData.transparencia} onChange={handleChange('transparencia')} {...limitProps('transparencia')} /></Grid>
            <Grid item xs={12} md={6}><TextField fullWidth label="Proatividade" value={formData.proatividade} onChange={handleChange('proatividade')} {...limitProps('proatividade')} /></Grid>
            <Grid item xs={12} md={6}><TextField fullWidth label="Cooperação" value={formData.cooperacao} onChange={handleChange('cooperacao')} {...limitProps('cooperacao')} /></Grid>
            <Grid item xs={12} md={4}><TextField fullWidth label="Resultado 1" value={formData.resultado_1} onChange={handleChange('resultado_1')} {...limitProps('resultado_1')} /></Grid>
            <Grid item xs={12} md={4}><TextField fullWidth label="Resultado 2" value={formData.resultado_2} onChange={handleChange('resultado_2')} {...limitProps('resultado_2')} /></Grid>
            <Grid item xs={12} md={4}><TextField fullWidth label="Resultado 3" value={formData.resultado_3} onChange={handleChange('resultado_3')} {...limitProps('resultado_3')} /></Grid>
            <Grid item xs={12}><TextField fullWidth label="Comprovação dos Resultados" value={formData.comprovacao_dos_resultados} onChange={handleChange('comprovacao_dos_resultados')} {...limitProps('comprovacao_dos_resultados')} /></Grid>
            <Grid item xs={12} md={6}><TextField fullWidth label="Categoria" value={formData.categoria} onChange={handleChange('categoria')} {...limitProps('categoria')} /></Grid>

            {/* Capa da iniciativa */}
            <Grid item xs={12} md={6}>
              <Button component="label" variant="outlined">
                Selecionar Capa
                <input type="file" accept="image/*" hidden onChange={(e)=> setCoverFile(e.target.files?.[0] || null)} />
              </Button>
              {coverFile && <Typography variant="caption" sx={{ ml: 1 }}>{coverFile.name}</Typography>}
            </Grid>

            {/* Anexos */}
            <Grid item xs={12} md={6}>
              <Button component="label" variant="outlined">
                Selecionar Anexos
                <input type="file" multiple hidden onChange={(e)=> setAttachmentFiles(Array.from(e.target.files || []))} />
              </Button>
              {attachmentFiles && attachmentFiles.length > 0 && (
                <Typography variant="caption" sx={{ ml: 1 }}>{attachmentFiles.length} arquivo(s) selecionado(s)</Typography>
              )}
            </Grid>

            {/* Equipe do Projeto */}
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom sx={{ color: 'primary.main', fontWeight: 'bold', mt: 4 }}>
                👥 2. Equipe do Projeto
              </Typography>
              <Divider sx={{ mb: 2, borderColor: 'rgba(0,0,0,0.08)' }} />
              <Stack spacing={2}>
                {members.map((m, idx)=> (
                  <Grid key={idx} container spacing={1} alignItems="center">
                    <Grid item xs={12} md={4}><TextField fullWidth label="Nome" value={m.name} onChange={(e)=> setMembers(prev=> prev.map((x,i)=> i===idx? {...x, name:e.target.value} : x))} /></Grid>
                    <Grid item xs={12} md={4}><TextField fullWidth label="Email" value={m.email} onChange={(e)=> setMembers(prev=> prev.map((x,i)=> i===idx? {...x, email:e.target.value} : x))} /></Grid>
                    <Grid item xs={12} md={3}><TextField fullWidth label="Papel" value={m.role} onChange={(e)=> setMembers(prev=> prev.map((x,i)=> i===idx? {...x, role:e.target.value} : x))} /></Grid>
                    <Grid item xs={12} md={1}><IconButton color="error" onClick={()=> setMembers(prev=> prev.filter((_,i)=> i!==idx))}><Delete/></IconButton></Grid>
            </Grid>
                ))}
                <Box>
                  <Button startIcon={<Add/>} onClick={()=> setMembers(prev=> [...prev, { name:'', email:'', role:'' }])}>Adicionar membro</Button>
                </Box>
              </Stack>
            </Grid>

            <Grid item xs={12}>
              <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end', mt: 4 }}>
                <Button variant="outlined" startIcon={<ArrowBack />} onClick={() => navigate('/projects')} disabled={saving}>Cancelar</Button>
                <Button type="submit" variant="contained" startIcon={<Save />} disabled={saving} size="large">
                  {saving ? 'Salvando...' : (isEdit ? 'Atualizar Projeto' : 'Criar Projeto')}
                </Button>
              </Box>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Container>
  )
}

export default ProjectForm 
