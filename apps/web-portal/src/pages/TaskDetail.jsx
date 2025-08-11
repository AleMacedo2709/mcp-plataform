import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Box, Typography, Paper, Stack, Chip, Button } from '@mui/material'
import Layout from '../components/Layout'
import { getTask } from '../services/taskDetailService'

export default function TaskDetail() {
  const { id } = useParams()
  const [task, setTask] = useState(null)
  const [err, setErr] = useState(null)
  const navigate = useNavigate()

  useEffect(()=>{
    let mounted = true
    const pull = async () => {
      try {
        const t = await getTask(id)
        if (mounted) setTask(t)
      } catch(e){ if (mounted) setErr(e.message) }
    }
    pull()
    const iv = setInterval(pull, 3000)
    return ()=> { mounted=false; clearInterval(iv) }
  }, [id])

  const parsedResult = (()=>{
    if (!task?.result) return null
    try {
      return JSON.parse(task.result)
    } catch { return null }
  })()

  return (
    <Layout>
      <Typography variant="h5" sx={{ mb: 2 }}>Tarefa #{id?.slice(0,8)}</Typography>
      {err && <Typography color="error">{err}</Typography>}
      {!task ? <div>Carregando…</div> :
        <Paper sx={{ p: 2 }}>
          <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
            <Chip label={task.status} />
            <Box>{task.type} — {task.filename}</Box>
          </Stack>
          <Typography variant="subtitle1">Resultado</Typography>
          <pre style={{ whiteSpace:'pre-wrap' }}>{task.result}</pre>
          {task.status==='success' && parsedResult &&
            <Button variant="contained" sx={{ mt: 2 }} onClick={()=>{
              navigate('/projects/new', { state: { prefill: parsedResult } })
            }}>Criar projeto a partir do resultado</Button>
          }
        </Paper>
      }
    </Layout>
  )
}
