import React, { useEffect, useState } from 'react'
import { Box, Typography, Grid, TextField, IconButton, Button, Paper, Divider } from '@mui/material'
import { Add, Delete } from '@mui/icons-material'
import { API_BASE_URL, projectService } from '../../services/apiService'

export default function ContactsTab({ projectId, canEdit = true }) {
  const [contacts, setContacts] = useState([])
  const [newContact, setNewContact] = useState({ nome:'', email:'' })
  const [loading, setLoading] = useState(true)

  const load = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE_URL}/projects/${projectId}/contacts`)
      const data = await res.json()
      setContacts(Array.isArray(data) ? data : [])
    } catch { setContacts([]) } finally { setLoading(false) }
  }

  useEffect(()=>{ load() },[projectId])

  const add = async () => {
    if (!newContact.nome?.trim() || !newContact.email?.trim()) return
    await fetch(`${API_BASE_URL}/projects/${projectId}/contacts`, {
      method:'POST', headers:{ 'Content-Type':'application/json', ...projectService.headers('editor') }, body: JSON.stringify(newContact)
    })
    setNewContact({ nome:'', email:'' })
    load()
  }

  const updateField = (idx, field, value) => {
    setContacts(prev => prev.map((c,i)=> i===idx ? { ...c, [field]: value } : c))
  }

  const save = async (contact) => {
    await fetch(`${API_BASE_URL}/projects/${projectId}/contacts/${contact.id}`, {
      method:'PUT', headers:{ 'Content-Type':'application/json', ...projectService.headers('editor') }, body: JSON.stringify({ nome: contact.nome, email: contact.email })
    })
  }

  const remove = async (id) => {
    await fetch(`${API_BASE_URL}/projects/${projectId}/contacts/${id}`, { method:'DELETE', headers: projectService.headers('editor') })
    load()
  }

  return (
    <Paper sx={{ p:2 }}>
      <Typography variant="h6" gutterBottom>Contatos</Typography>
      <Divider sx={{ mb:2 }} />

      <Grid container spacing={2}>
        {contacts.map((c, idx)=> (
          <React.Fragment key={c.id}>
            <Grid item xs={12} md={6}><TextField fullWidth label="Nome" value={c.nome||''} onChange={(e)=> updateField(idx,'nome',e.target.value)} onBlur={()=> save(contacts[idx])} /></Grid>
            <Grid item xs={12} md={5}><TextField fullWidth label="Email" value={c.email||''} onChange={(e)=> updateField(idx,'email',e.target.value)} onBlur={()=> save(contacts[idx])} /></Grid>
            {canEdit && <Grid item xs={12} md={1}><IconButton color="error" onClick={()=> remove(c.id)}><Delete/></IconButton></Grid>}
          </React.Fragment>
        ))}
      </Grid>

      {canEdit && <Box sx={{ mt:3 }}>
        <Typography variant="subtitle1" gutterBottom>Novo Contato</Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}><TextField fullWidth label="Nome" value={newContact.nome} onChange={(e)=> setNewContact(prev=> ({...prev, nome:e.target.value}))} /></Grid>
          <Grid item xs={12} md={5}><TextField fullWidth label="Email" value={newContact.email} onChange={(e)=> setNewContact(prev=> ({...prev, email:e.target.value}))} /></Grid>
          <Grid item xs={12} md={1}><Button startIcon={<Add/>} variant="contained" onClick={add}>Adicionar</Button></Grid>
        </Grid>
      </Box>}
    </Paper>
  )
}


