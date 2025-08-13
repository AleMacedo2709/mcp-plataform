import React from 'react'
import { Grid, TextField, IconButton, Box, Button, FormControl, InputLabel, Select, MenuItem, Stack, Typography, Divider } from '@mui/material'
import { Add, Delete } from '@mui/icons-material'
import { papelEquipeOptions as PAPEL_EQUIPE } from '../constants/formOptions'

export default function TeamFields({ members, setMembers, title = '👥 Equipe da Iniciativa', showDivider = true, size = 'small' }) {
  return (
    <>
      {showDivider && (
        <>
          <Divider sx={{ my: 2 }} />
          <Typography variant="h6" gutterBottom sx={{ color: 'primary.main', fontWeight: 'bold' }}>{title}</Typography>
        </>
      )}
      <Stack spacing={2}>
        {members.map((m, idx)=> (
          <Grid key={idx} container spacing={1} alignItems="center">
            <Grid item xs={12} md={4}><TextField fullWidth size={size} label="Nome" value={m.name} onChange={(e)=> setMembers(prev=> prev.map((x,i)=> i===idx? { ...x, name:e.target.value } : x))} /></Grid>
            <Grid item xs={12} md={4}><TextField fullWidth size={size} label="Email" value={m.email} onChange={(e)=> setMembers(prev=> prev.map((x,i)=> i===idx? { ...x, email:e.target.value } : x))} /></Grid>
            <Grid item xs={12} md={3} sx={{ display:'flex', alignItems:'center' }}>
              <FormControl fullWidth size={size}>
                <InputLabel id={`team-role-label-${idx}`}>Papel</InputLabel>
                <Select labelId={`team-role-label-${idx}`} id={`team-role-${idx}`} value={m.role} label="Papel" onChange={(e)=> setMembers(prev=> prev.map((x,i)=> i===idx? { ...x, role:e.target.value } : x))}>
                  {PAPEL_EQUIPE.map((p)=> (<MenuItem key={p} value={p}>{p}</MenuItem>))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={1} sx={{ display:'flex', alignItems:'center', justifyContent:{ xs:'flex-start', md:'center' } }}>
              <IconButton color="error" onClick={()=> setMembers(prev=> prev.filter((_,i)=> i!==idx))}><Delete/></IconButton>
            </Grid>
          </Grid>
        ))}
        <Box>
          <Button startIcon={<Add/>} onClick={()=> setMembers(prev=> [...prev, { name:'', email:'', role:'' }])}>Adicionar membro</Button>
        </Box>
      </Stack>
    </>
  )
}


