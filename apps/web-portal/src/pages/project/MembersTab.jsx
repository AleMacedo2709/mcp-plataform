import React, { useEffect, useState } from 'react'
import { Box, Typography, Stack, TextField, Button, IconButton, Paper } from '@mui/material'
import { Delete } from '@mui/icons-material'
import { API_BASE_URL, projectService } from '../../services/apiService'

export default function MembersTab({ projectId, canEdit = true }) {
  const [rows, setRows] = useState([])
  const [form, setForm] = useState({ name: '', email: '', role: '' })

  const load = async () => {
    const r = await fetch(`${API_BASE_URL}/projects/${projectId}/members`).then(r=>r.json()).catch(()=>[])
    setRows(r||[])
  }
  useEffect(()=>{ if(projectId) load() }, [projectId])

  const add = async () => {
    if(!form.name.trim() || !form.email.trim()) return
    await fetch(`${API_BASE_URL}/projects/${projectId}/members`, { method:'POST', headers:{ 'Content-Type':'application/json', ...projectService.headers('editor') }, body: JSON.stringify(form) })
    setForm({ name:'', email:'', role:'' }); await load()
  }

  const remove = async (id) => {
    await fetch(`${API_BASE_URL}/projects/${projectId}/members/${id}`, { method:'DELETE', headers: projectService.headers('editor') }); await load()
  }

  return (
    <Paper variant='outlined' sx={{ p:2 }}>
      <Typography variant='h6' sx={{ mb: 2, fontWeight: 700 }}>Equipe da Iniciativa</Typography>
      <Stack direction='row' spacing={1} sx={{ mb:2, display: canEdit ? 'flex' : 'none' }}>
        <TextField size='small' label='Nome' value={form.name} onChange={(e)=>setForm({...form, name:e.target.value})} />
        <TextField size='small' label='Email' value={form.email} onChange={(e)=>setForm({...form, email:e.target.value})} />
        <TextField size='small' label='Papel' value={form.role} onChange={(e)=>setForm({...form, role:e.target.value})} />
        <Button variant='contained' onClick={add}>Adicionar</Button>
      </Stack>
      <Stack spacing={1}>
        {rows.map(m=> (
          <Stack key={m.id} direction='row' alignItems='center' spacing={2}>
            <Box sx={{ flex:1 }}>
              <Typography variant='subtitle2'>{m.name}</Typography>
              <Typography variant='caption' color='text.secondary'>{m.email} · {m.role||'—'}</Typography>
            </Box>
            {canEdit && <IconButton color='error' size='small' onClick={()=>remove(m.id)}><Delete/></IconButton>}
          </Stack>
        ))}
        {rows.length===0 && <Typography variant='body2' color='text.secondary'>Nenhum membro adicionado</Typography>}
      </Stack>
    </Paper>
  )
}


