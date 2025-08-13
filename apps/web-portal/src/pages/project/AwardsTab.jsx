import React, { useEffect, useState } from 'react'
import { Box, Typography, Grid, TextField, Select, MenuItem, IconButton, Button, Paper, Divider } from '@mui/material'
import { Add, Delete } from '@mui/icons-material'
import { API_BASE_URL, projectService } from '../../services/apiService'
import { premioCnmpCategorias } from '../../constants/formOptions'

export default function AwardsTab({ projectId, canEdit = true }) {
  const [items, setItems] = useState([])
  const [newItem, setNewItem] = useState({ ano:'', categoria:'' })

  const load = async ()=> {
    try {
      const res = await fetch(`${API_BASE_URL}/projects/${projectId}/awards`)
      const data = await res.json(); setItems(Array.isArray(data)? data: [])
    } catch { setItems([]) }
  }
  useEffect(()=> { load() }, [projectId])

  const add = async ()=> {
    if (!newItem.ano || !newItem.categoria) return
    await fetch(`${API_BASE_URL}/projects/${projectId}/awards`, { method:'POST', headers:{ 'Content-Type':'application/json', ...projectService.headers('editor') }, body: JSON.stringify(newItem) })
    setNewItem({ ano:'', categoria:'' }); load()
  }

  const update = async (item)=> {
    await fetch(`${API_BASE_URL}/projects/${projectId}/awards/${item.id}`, { method:'PUT', headers:{ 'Content-Type':'application/json', ...projectService.headers('editor') }, body: JSON.stringify({ ano:item.ano, categoria:item.categoria }) })
  }

  const remove = async (id)=> {
    await fetch(`${API_BASE_URL}/projects/${projectId}/awards/${id}`, { method:'DELETE', headers: projectService.headers('editor') }); load()
  }

  return (
    <Paper sx={{ p:2 }}>
      <Typography variant="h6" gutterBottom>Prêmio CNMP</Typography>
      <Divider sx={{ mb:2 }} />

      <Grid container spacing={2}>
        {items.map((i)=> (
          <React.Fragment key={i.id}>
            <Grid item xs={6} md={3}><TextField fullWidth label="Ano" value={i.ano||''} onChange={(e)=> setItems(prev=> prev.map(x=> x.id===i.id? {...x, ano:e.target.value}: x))} onBlur={()=> update(items.find(x=> x.id===i.id))} /></Grid>
            <Grid item xs={6} md={4}>
              <Select fullWidth value={i.categoria||''} onChange={(e)=> setItems(prev=> prev.map(x=> x.id===i.id? {...x, categoria:e.target.value}: x))} onBlur={()=> update(items.find(x=> x.id===i.id))}>
                {premioCnmpCategorias.map(c=> <MenuItem key={c} value={c}>{c}</MenuItem>)}
              </Select>
            </Grid>
            {canEdit && <Grid item xs={12} md={1}><IconButton color="error" onClick={()=> remove(i.id)}><Delete/></IconButton></Grid>}
          </React.Fragment>
        ))}
      </Grid>

      {canEdit && (
        <Box sx={{ mt:3 }}>
          <Typography variant="subtitle1" gutterBottom>Novo Registro</Typography>
          <Grid container spacing={2}>
            <Grid item xs={6} md={3}><TextField fullWidth label="Ano" value={newItem.ano} onChange={(e)=> setNewItem(prev=> ({...prev, ano:e.target.value}))} /></Grid>
            <Grid item xs={6} md={4}>
              <Select fullWidth displayEmpty value={newItem.categoria} onChange={(e)=> setNewItem(prev=> ({...prev, categoria:e.target.value}))}>
                <MenuItem value=""><em>Categoria</em></MenuItem>
                {premioCnmpCategorias.map(c=> <MenuItem key={c} value={c}>{c}</MenuItem>)}
              </Select>
            </Grid>
            <Grid item xs={12} md={2}><Button startIcon={<Add/>} variant="contained" onClick={add}>Adicionar</Button></Grid>
          </Grid>
        </Box>
      )}
    </Paper>
  )
}


