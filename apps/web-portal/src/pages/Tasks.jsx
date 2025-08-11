import React, { useEffect, useState } from 'react'
import { Box, Typography, Paper, Stack, Chip } from '@mui/material'
import Layout from '../components/Layout'
import { listTasks } from '../services/tasksService'
import { Link } from 'react-router-dom'

export default function Tasks() {
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)
  useEffect(()=>{
    (async ()=>{
      try {
        const data = await listTasks({ owner: 'me' })
        setRows(data || [])
      } catch(e) { console.error(e) }
      finally { setLoading(false) }
    })()
  },[])
  return (
    <Layout>
      <Typography variant="h5" sx={{ mb: 2 }}>Processamentos</Typography>
      {loading? <div>Carregando…</div> :
      <Stack spacing={1}>
        {rows.map((t)=>(
          <Paper key={t.id} sx={{ p: 2 }}>
            <Stack direction="row" spacing={2} alignItems="center">
              <Box sx={{ fontFamily: 'monospace' }}>#{t.id.slice(0,8)}</Box>
              <Chip size="small" label={t.status} />
              <Box sx={{ flex:1 }}>{t.type} — {t.filename}</Box>
              <Box><Link to={`/tasks/${t.id}`}>detalhes</Link></Box>
            </Stack>
          </Paper>
        ))}
        {rows.length===0 && <Typography>Nenhuma tarefa encontrada.</Typography>}
      </Stack>}
    </Layout>
  )
}
