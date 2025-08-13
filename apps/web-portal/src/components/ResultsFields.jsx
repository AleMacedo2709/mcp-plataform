import React from 'react'
import { Grid, TextField, IconButton, Box, Button, Stack, Typography, Divider } from '@mui/material'
import { Add, Delete } from '@mui/icons-material'

export default function ResultsFields({ results, setResults, title = '✅ Comprovação dos Resultados', showDivider = true, size = 'small' }) {
  return (
    <>
      {showDivider && (
        <>
          <Divider sx={{ my: 2 }} />
          <Typography variant="h6" gutterBottom sx={{ color: 'primary.main', fontWeight: 'bold' }}>{title}</Typography>
        </>
      )}
      <Stack spacing={2}>
        {results.map((r, idx)=> (
          <Grid key={idx} container spacing={1} alignItems="center">
            <Grid item xs={12} md={4}><TextField fullWidth size={size} type="date" InputLabelProps={{shrink:true}} label="Data da Coleta" value={r.data_da_coleta} onChange={(e)=> setResults(prev=> prev.map((x,i)=> i===idx? { ...x, data_da_coleta:e.target.value } : x))} helperText=" " FormHelperTextProps={{ sx:{ visibility:'hidden' } }} /></Grid>
            <Grid item xs={12} md={7}><TextField fullWidth size={size} label="Resultado" inputProps={{ maxLength:200 }} helperText={`${(r.resultado||'').length}/200`} value={r.resultado} onChange={(e)=> setResults(prev=> prev.map((x,i)=> i===idx? { ...x, resultado:e.target.value } : x))} /></Grid>
            <Grid item xs={12} md={1} sx={{ display:'flex', alignItems:'center', justifyContent:{ xs:'flex-start', md:'flex-end' } }}>
              <IconButton color="error" onClick={()=> setResults(prev=> prev.filter((_,i)=> i!==idx))}><Delete/></IconButton>
            </Grid>
          </Grid>
        ))}
        <Box>
          <Button startIcon={<Add/>} onClick={()=> setResults(prev=> [...prev, { data_da_coleta:'', resultado:'' }])}>Adicionar comprovação</Button>
        </Box>
      </Stack>
    </>
  )
}


