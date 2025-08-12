import React, { useEffect, useState } from 'react'
import { Box, Card, CardContent, Typography, IconButton, Tooltip, Stack, Button } from '@mui/material'
import { Edit, Delete, Visibility, PictureAsPdf } from '@mui/icons-material'
import { projectService } from '../services/apiService'
import { useAuth } from '../hooks/useAuth'
import { useNavigate } from 'react-router-dom'

export default function MyProjects() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(()=>{ load() },[])

  const load = async ()=>{
    try {
      setLoading(true)
      const res = await projectService.getAll({ search: user?.email })
      const mapped = (res.projects || []).map(p=> ({
        ...p,
        nome_iniciativa: p.nome_da_iniciativa || p.nome_iniciativa,
        tipo_iniciativa: p.tipo_de_iniciativa || p.tipo_iniciativa,
        fase: p.fase_de_implementacao || p.fase_implementacao || p.fase
      }))
      setRows(mapped)
    } finally { setLoading(false) }
  }

  const printPdf = (p)=>{
    const data = JSON.stringify(p, null, 2)
    const blob = new Blob([data], {type:'application/json'})
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a'); a.href=url; a.download=`projeto-${p.id}.json`; a.click(); URL.revokeObjectURL(url)
  }

  return (
    <Box>
      <Stack direction='row' justifyContent='space-between' alignItems='center' sx={{ mb: 2 }}>
        <Typography variant='h5' sx={{ fontWeight: 800 }}>Meus Projetos</Typography>
        <Button variant='contained' onClick={()=>navigate('/projects/new')}>Novo Projeto</Button>
      </Stack>
      {loading? <Typography>Carregando…</Typography> : (
        <Stack spacing={1}>
          {(rows||[]).map((p)=>(
            <Card key={p.id} variant='outlined'>
              <CardContent>
                <Stack direction='row' alignItems='center' spacing={2}>
                  <Box sx={{ flex:1 }}>
                    <Typography variant='subtitle1' sx={{ fontWeight: 600 }}>{p.nome_iniciativa}</Typography>
                    <Typography variant='caption' color='text.secondary'>#{p.id} · {p.tipo_iniciativa} · {p.fase || p.fase_de_implementacao || '—'}</Typography>
                  </Box>
                  <Tooltip title='Visualizar'><IconButton onClick={()=>navigate(`/projects/${p.id}`)}><Visibility/></IconButton></Tooltip>
                  <Tooltip title='Editar'><IconButton color='primary' onClick={()=>navigate(`/projects/${p.id}/edit`)}><Edit/></IconButton></Tooltip>
                  <Tooltip title='Imprimir/Exportar'><IconButton onClick={()=>printPdf(p)}><PictureAsPdf/></IconButton></Tooltip>
                  <Tooltip title='Excluir'>
                    <IconButton color='error' onClick={async()=>{ if(!window.confirm('Excluir projeto?')) return; await projectService.delete(p.id); await load() }}><Delete/></IconButton>
                  </Tooltip>
                </Stack>
              </CardContent>
            </Card>
          ))}
          {(!rows || rows.length===0) && <Typography className='text-muted'>Nenhum projeto encontrado</Typography>}
        </Stack>
      )}
    </Box>
  )
}


