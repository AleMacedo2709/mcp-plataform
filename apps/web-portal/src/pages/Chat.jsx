import React, { useEffect, useRef, useState } from 'react'
import { Box, Paper, Typography, TextField, IconButton, Stack, Chip, Button } from '@mui/material'
import SendIcon from '@mui/icons-material/Send'
import Layout from '../components/Layout'
import { Card, CardContent, CardActions, Button } from '@mui/material'
import { Link as RouterLink, useNavigate } from 'react-router-dom'

function MessageView({ msg }) {
  if (msg.role !== 'assistant') return <Box sx={{ whiteSpace:'pre-wrap' }}><b>{msg.role}:</b> {msg.content}</Box>
  let payload = {}
  try { payload = JSON.parse(msg.content) } catch {}
  if (payload?.results || payload?.hits || payload?.data) {
    return (
      <Stack spacing={2}>
        {payload.results && (
          <>
            <Typography variant="subtitle1">Projetos encontrados</Typography>
            {payload.results.map((r, idx) => (
              <Card key={idx} variant="outlined">
                <CardContent>
                  <Typography variant="h6">#{r.id} {r.nome_da_iniciativa}</Typography>
                  <Typography variant="body2" color="text.secondary">Fase: {r.fase_de_implementacao || '—'}</Typography>
                  <Typography variant="body2" sx={{ mt: 1 }}>{r.descricao?.slice(0,200)}</Typography>
                </CardContent>
                <CardActions>
                  <Button size="small" component={RouterLink} to={`/projects/${r.id}`}>Ver projeto</Button>
                </CardActions>
              </Card>
            ))}
          </>
        )}
        {payload.hits && (
          <>
            <Typography variant="subtitle1">Resources</Typography>
            {payload.hits.map((h, i) => (
              <Card key={i} variant="outlined">
                <CardContent>
                  <Typography variant="body2" sx={{ fontFamily:'monospace', whiteSpace:'pre-wrap' }}>{h.snippet}</Typography>
                  <Typography variant="caption" color="text.secondary">Arquivo: {h.file}</Typography>
                </CardContent>
              </Card>
            ))}
          </>
        )}
        {payload.data && (
          <Card variant="outlined">
            <CardContent>
              <Typography variant="h6">Projeto</Typography>
              <Typography variant="subtitle2">{payload.data.nome_da_iniciativa}</Typography>
              <Typography variant="body2" sx={{ mt:1 }}>{payload.data.descricao}</Typography>
            </CardContent>
            <CardActions>
              <Button size="small" component={RouterLink} to={`/projects/${payload.data.id}`}>Ver projeto</Button>
            </CardActions>
          </Card>
        )}
        {payload.analysis && (
          <Card variant="outlined">
            <CardContent>
              <Typography variant="h6">Sugestão de campos</Typography>
              <pre style={{ whiteSpace:'pre-wrap' }}>{JSON.stringify(payload.analysis, null, 2)}</pre>
            </CardContent>
            <CardActions>
              <PrefillButton suggested={payload.analysis} />
            </CardActions>
          </Card>
        )}
      </Stack>
    )
  }
  return <Box sx={{ whiteSpace:'pre-wrap', fontFamily:'monospace' }}><b>{msg.role}:</b> {msg.content}</Box>
}

function PrefillButton({ suggested }) {
  const navigate = useNavigate()
  const onClick = () => {
    // Navega para ProjectForm com estado inicial
    navigate('/projects/new', { state: { prefill: suggested } })
  }
  return <Button onClick={onClick} variant="contained">Criar projeto a partir da resposta</Button>
}

import { createChatSocket, chatAsk } from '../services/chatService'

export default function Chat() {
  const [messages, setMessages] = useState([
    { role: 'system', content: 'Bem-vindo! Pergunte sobre projetos, campos do CNMP ou recursos.' }
  ])
  const [input, setInput] = useState('')
  const [chips, setChips] = useState([])
  const [lastAssistant, setLastAssistant] = useState(null)
  const wsRef = useRef(null)
  const [wsReady, setWsReady] = useState(false)

  useEffect(() => {
    const ws = createChatSocket()
    wsRef.current = ws
    ws.onopen = () => setWsReady(true)
    ws.onclose = () => setWsReady(false)
    ws.onerror = () => setWsReady(false)
    ws.onmessage = (evt) => {
      try {
        const data = JSON.parse(evt.data)
        if (data.type === 'answer') {
          const content = JSON.stringify(data.payload, null, 2); setMessages((prev) => [...prev, { role: 'assistant', content }]); setLastAssistant(content)
        } else if (data.type === 'welcome') {
          setMessages((prev) => [...prev, { role: 'system', content: data.message }])
        }
      } catch (e) { /* ignore */ }
    }
    return () => ws.close()
  }, [])

  const send = async () => {
    if (!input.trim()) return
    const q = input.trim()
    setMessages((prev) => [...prev, { role: 'user', content: q }])
    setInput('')
    // Try WS first
    const ws = wsRef.current
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ question: q }))
      return
    }
    // Fallback HTTP
    try {
      const res = await chatAsk(q)
      const content = JSON.stringify(res, null, 2); setMessages((prev) => [...prev, { role: 'assistant', content }]); setLastAssistant(content)
    } catch (e) {
      setMessages((prev) => [...prev, { role: 'system', content: 'Falha ao enviar: ' + e.message }])
    }
  }

  return (
    <Layout>
      <Typography variant="h5" sx={{ mb: 2 }}>Chat (MCP)</Typography>
      <Stack direction="row" spacing={1} sx={{ mb: 1, flexWrap:'wrap' }}>
        {['projeto','resource','documento','buscar'].map((t)=>(
          <Chip key={t} label={t} onClick={()=>setInput((v)=> (v? (v+ ' ' + t) : t))} />
        ))}
        <Box sx={{ flexGrow:1 }} />
        <Button size="small" variant="outlined" disabled={!lastAssistant} onClick={()=>{
          if(!lastAssistant) return;
          const blob = new Blob([lastAssistant], {type:'application/json'});
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a'); a.href=url; a.download='chat-resposta.json'; a.click(); URL.revokeObjectURL(url);
        }}>Exportar resposta</Button>
      </Stack>
      <Paper variant="outlined" sx={{ p: 2, height: 480, overflowY: 'auto', mb: 2, bgcolor: '#fff' }}>
        <Stack spacing={1}>
          {messages.map((m, i) => (
            <Box key={i}>
              <MessageView msg={m} />
            </Box>
          ))}
        </Stack>
      </Paper>
      <Stack direction="row" spacing={1}>
        <TextField
          fullWidth
          placeholder={wsReady ? 'Digite sua pergunta…' : 'WS indisponível, enviarei por HTTP'}
          value={input}
          onChange={(e)=>setInput(e.target.value)}
          onKeyDown={(e)=>{ if(e.key==='Enter') send() }}
        />
        <IconButton color="primary" onClick={send}><SendIcon /></IconButton>
      </Stack>
    </Layout>
  )
}
