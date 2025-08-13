import React, { useEffect, useState } from 'react'
import { Box, Typography, Button, Grid, TextField, Select, MenuItem, IconButton, Paper, Divider } from '@mui/material'
import { Add, Delete } from '@mui/icons-material'
import { API_BASE_URL, projectService } from '../../services/apiService'

const statusOptions = ['Não iniciada','Em andamento','Concluída','Suspensa']

export default function ActionsTab({ projectId, canEdit = true }) {
  const [actions, setActions] = useState([])
  const [newAction, setNewAction] = useState({ descricao:'', area_responsavel:'', email_responsavel:'', progresso:'', inicio_previsto:'', termino_previsto:'', inicio_efetivo:'', termino_efetivo:'' })
  const [loading, setLoading] = useState(true)

  const load = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE_URL}/projects/${projectId}/actions`)
      const data = await res.json()
      setActions(Array.isArray(data) ? data : [])
    } catch {
      setActions([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(()=>{ load() },[projectId])

  const add = async () => {
    if (!newAction.descricao?.trim()) return
    await fetch(`${API_BASE_URL}/projects/${projectId}/actions`, { method:'POST', headers:{ 'Content-Type':'application/json', ...projectService.headers('editor') }, body: JSON.stringify(newAction) })
    setNewAction({ descricao:'', area_responsavel:'', email_responsavel:'', progresso:'', inicio_previsto:'', termino_previsto:'', inicio_efetivo:'', termino_efetivo:'' })
    load()
  }

  const remove = async (id) => {
    await fetch(`${API_BASE_URL}/projects/${projectId}/actions/${id}`, { method:'DELETE', headers: projectService.headers('editor') })
    load()
  }

  const updateField = (idx, field, value) => {
    setActions(prev => prev.map((a,i)=> i===idx ? { ...a, [field]: value } : a))
  }

  const save = async (action) => {
    await fetch(`${API_BASE_URL}/projects/${projectId}/actions/${action.id}`, { method:'PUT', headers:{ 'Content-Type':'application/json', ...projectService.headers('editor') }, body: JSON.stringify(action) })
    load()
  }

  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>Ações da Iniciativa</Typography>
      <Divider sx={{ mb: 2 }} />

      {/* Lista existente */}
      <Grid container spacing={2}>
        {actions.map((a, idx)=> (
          <React.Fragment key={a.id}>
            <Grid item xs={12} md={4}><TextField fullWidth label="Ação (descritivo)" value={a.descricao||''} onChange={(e)=> updateField(idx,'descricao',e.target.value)} onBlur={()=> save(actions[idx])}/></Grid>
            <Grid item xs={12} md={3}><TextField fullWidth label="Área Responsável" value={a.area_responsavel||''} onChange={(e)=> updateField(idx,'area_responsavel',e.target.value)} onBlur={()=> save(actions[idx])}/></Grid>
            <Grid item xs={12} md={3}><TextField fullWidth label="Email Responsável" value={a.email_responsavel||''} onChange={(e)=> updateField(idx,'email_responsavel',e.target.value)} onBlur={()=> save(actions[idx])}/></Grid>
            <Grid item xs={12} md={2}>
              <Select fullWidth displayEmpty value={a.progresso||''} onChange={(e)=> updateField(idx,'progresso',e.target.value)} onBlur={()=> save(actions[idx])}>
                <MenuItem value=""><em>Progresso</em></MenuItem>
                {statusOptions.map(s=> <MenuItem key={s} value={s}>{s}</MenuItem>)}
              </Select>
            </Grid>
            <Grid item xs={6} md={3}><TextField fullWidth label="Início Previsto" type="date" InputLabelProps={{shrink:true}} value={a.inicio_previsto||''} onChange={(e)=> updateField(idx,'inicio_previsto',e.target.value)} onBlur={()=> save(actions[idx])}/></Grid>
            <Grid item xs={6} md={3}><TextField fullWidth label="Término Previsto" type="date" InputLabelProps={{shrink:true}} value={a.termino_previsto||''} onChange={(e)=> updateField(idx,'termino_previsto',e.target.value)} onBlur={()=> save(actions[idx])}/></Grid>
            <Grid item xs={6} md={3}><TextField fullWidth label="Início Efetivo" type="date" InputLabelProps={{shrink:true}} value={a.inicio_efetivo||''} onChange={(e)=> updateField(idx,'inicio_efetivo',e.target.value)} onBlur={()=> save(actions[idx])}/></Grid>
            <Grid item xs={6} md={2}><TextField fullWidth label="Término Efetivo" type="date" InputLabelProps={{shrink:true}} value={a.termino_efetivo||''} onChange={(e)=> updateField(idx,'termino_efetivo',e.target.value)} onBlur={()=> save(actions[idx])}/></Grid>
            {canEdit && <Grid item xs={12} md={1}><IconButton color="error" onClick={()=> remove(a.id)}><Delete/></IconButton></Grid>}
          </React.Fragment>
        ))}
      </Grid>

      {/* Nova ação */}
      {canEdit && <Box sx={{ mt: 3 }}>
        <Typography variant="subtitle1" gutterBottom>Nova Ação</Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}><TextField fullWidth label="Ação (descritivo)" value={newAction.descricao} onChange={(e)=> setNewAction(prev=> ({...prev, descricao:e.target.value}))} /></Grid>
          <Grid item xs={12} md={3}><TextField fullWidth label="Área Responsável" value={newAction.area_responsavel} onChange={(e)=> setNewAction(prev=> ({...prev, area_responsavel:e.target.value}))} /></Grid>
          <Grid item xs={12} md={3}><TextField fullWidth label="Email Responsável" value={newAction.email_responsavel} onChange={(e)=> setNewAction(prev=> ({...prev, email_responsavel:e.target.value}))} /></Grid>
          <Grid item xs={12} md={2}>
            <Select fullWidth displayEmpty value={newAction.progresso} onChange={(e)=> setNewAction(prev=> ({...prev, progresso:e.target.value}))}>
              <MenuItem value=""><em>Progresso</em></MenuItem>
              {statusOptions.map(s=> <MenuItem key={s} value={s}>{s}</MenuItem>)}
            </Select>
          </Grid>
          <Grid item xs={6} md={3}><TextField fullWidth label="Início Previsto" type="date" InputLabelProps={{shrink:true}} value={newAction.inicio_previsto} onChange={(e)=> setNewAction(prev=> ({...prev, inicio_previsto:e.target.value}))} /></Grid>
          <Grid item xs={6} md={3}><TextField fullWidth label="Término Previsto" type="date" InputLabelProps={{shrink:true}} value={newAction.termino_previsto} onChange={(e)=> setNewAction(prev=> ({...prev, termino_previsto:e.target.value}))} /></Grid>
          <Grid item xs={6} md={3}><TextField fullWidth label="Início Efetivo" type="date" InputLabelProps={{shrink:true}} value={newAction.inicio_efetivo} onChange={(e)=> setNewAction(prev=> ({...prev, inicio_efetivo:e.target.value}))} /></Grid>
          <Grid item xs={6} md={2}><TextField fullWidth label="Término Efetivo" type="date" InputLabelProps={{shrink:true}} value={newAction.termino_efetivo} onChange={(e)=> setNewAction(prev=> ({...prev, termino_efetivo:e.target.value}))} /></Grid>
          <Grid item xs={12} md={1}><Button startIcon={<Add/>} variant="contained" onClick={add}>Adicionar</Button></Grid>
        </Grid>
      </Box>}
    </Paper>
  )
}


