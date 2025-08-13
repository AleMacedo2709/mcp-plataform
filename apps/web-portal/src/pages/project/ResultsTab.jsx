import React, { useEffect, useState } from 'react'
import { Box, Typography, Grid, TextField, IconButton, Button, Paper, Divider } from '@mui/material'
import { Add, Delete } from '@mui/icons-material'
import { API_BASE_URL, projectService } from '../../services/apiService'

export default function ResultsTab({ projectId, canEdit = true }) {
  const [items, setItems] = useState([])
  const [newItem, setNewItem] = useState({ data_da_coleta:'', resultado:'' })
  const [loading, setLoading] = useState(true)

  const load = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE_URL}/projects/${projectId}/results`)
      const data = await res.json()
      setItems(Array.isArray(data) ? data : [])
    } catch { setItems([]) } finally { setLoading(false) }
  }

  useEffect(()=>{ load() },[projectId])

  const add = async () => {
    if (!newItem.resultado?.trim()) return
    await fetch(`${API_BASE_URL}/projects/${projectId}/results`, {
      method:'POST', headers:{ 'Content-Type':'application/json', ...projectService.headers('editor') }, body: JSON.stringify(newItem)
    })
    setNewItem({ data_da_coleta:'', resultado:'' })
    load()
  }

  const updateField = (idx, field, value) => {
    setItems(prev => prev.map((i,j)=> j===idx ? { ...i, [field]: value } : i))
  }

  const save = async (item) => {
    await fetch(`${API_BASE_URL}/projects/${projectId}/results/${item.id}`, {
      method:'PUT', headers:{ 'Content-Type':'application/json', ...projectService.headers('editor') }, body: JSON.stringify({ data_da_coleta: item.data_da_coleta, resultado: item.resultado })
    })
  }

  const remove = async (id) => {
    await fetch(`${API_BASE_URL}/projects/${projectId}/results/${id}`, { method:'DELETE', headers: projectService.headers('editor') })
    load()
  }

  return (
    <Paper sx={{ p:2 }}>
      <Typography variant="h6" gutterBottom>Comprovação dos Resultados</Typography>
      <Divider sx={{ mb:2 }} />

      <Grid container spacing={2}>
        {items.map((r, idx)=> (
          <React.Fragment key={r.id}>
            <Grid item xs={12} md={4}><TextField fullWidth type="date" InputLabelProps={{shrink:true}} label="Data da Coleta" value={r.data_da_coleta||''} onChange={(e)=> updateField(idx,'data_da_coleta',e.target.value)} onBlur={()=> save(items[idx])} /></Grid>
            <Grid item xs={12} md={7}><TextField fullWidth label="Resultado" inputProps={{ maxLength:200 }} helperText={`${(r.resultado||'').length}/200`} value={r.resultado||''} onChange={(e)=> updateField(idx,'resultado',e.target.value)} onBlur={()=> save(items[idx])} /></Grid>
            {canEdit && <Grid item xs={12} md={1}><IconButton color="error" onClick={()=> remove(r.id)}><Delete/></IconButton></Grid>}
          </React.Fragment>
        ))}
      </Grid>

      {canEdit && <Box sx={{ mt:3 }}>
        <Typography variant="subtitle1" gutterBottom>Novo Resultado</Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}><TextField fullWidth type="date" InputLabelProps={{shrink:true}} label="Data da Coleta" value={newItem.data_da_coleta} onChange={(e)=> setNewItem(prev=> ({...prev, data_da_coleta:e.target.value}))} /></Grid>
          <Grid item xs={12} md={7}><TextField fullWidth label="Resultado" inputProps={{ maxLength:200 }} helperText={`${(newItem.resultado||'').length}/200`} value={newItem.resultado} onChange={(e)=> setNewItem(prev=> ({...prev, resultado:e.target.value}))} /></Grid>
          <Grid item xs={12} md={1}><Button startIcon={<Add/>} variant="contained" onClick={add}>Adicionar</Button></Grid>
        </Grid>
      </Box>}
    </Paper>
  )
}


