import React from 'react'
import { Grid, TextField, IconButton, Box, Button, Stack, Typography, Divider } from '@mui/material'
import { Add, Delete } from '@mui/icons-material'

export default function ContactsFields({ contacts, setContacts, title = '📞 Contatos', showDivider = true, size = 'small' }) {
  return (
    <>
      {showDivider && (
        <>
          <Divider sx={{ my: 2 }} />
          <Typography variant="h6" gutterBottom sx={{ color: 'primary.main', fontWeight: 'bold' }}>{title}</Typography>
        </>
      )}
      <Stack spacing={2}>
        {contacts.map((c, idx)=> (
          <Grid key={idx} container spacing={1} alignItems="center">
            <Grid item xs={12} md={6}><TextField fullWidth size={size} label="Nome" value={c.nome} onChange={(e)=> setContacts(prev=> prev.map((x,i)=> i===idx? { ...x, nome:e.target.value } : x))} /></Grid>
            <Grid item xs={12} md={5}><TextField fullWidth size={size} label="Email" value={c.email} onChange={(e)=> setContacts(prev=> prev.map((x,i)=> i===idx? { ...x, email:e.target.value } : x))} /></Grid>
            <Grid item xs={12} md={1} sx={{ display:'flex', alignItems:'center', justifyContent:{ xs:'flex-start', md:'center' } }}>
              <IconButton color="error" onClick={()=> setContacts(prev=> prev.filter((_,i)=> i!==idx))}><Delete/></IconButton>
            </Grid>
          </Grid>
        ))}
        <Box>
          <Button startIcon={<Add/>} onClick={()=> setContacts(prev=> [...prev, { nome:'', email:'' }])}>Adicionar contato</Button>
        </Box>
      </Stack>
    </>
  )
}


