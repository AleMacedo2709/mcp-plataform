import React from 'react'
import { AppBar, Toolbar, Typography, Container, Box, Button, Avatar, useTheme, useMediaQuery, IconButton, Menu, MenuItem, Divider } from '@mui/material'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import MenuIcon from '@mui/icons-material/Menu'

export default function Layout({ children }) {
  const navigate = useNavigate()
  const theme = useTheme()
  const isSmall = useMediaQuery(theme.breakpoints.down('md'))
  const [menuEl, setMenuEl] = React.useState(null)
  const openMenu = (e) => setMenuEl(e.currentTarget)
  const closeMenu = () => setMenuEl(null)
  const { pathname } = useLocation()

  const isActive = (matcher) => matcher(pathname)
  const active = {
    dashboard: isActive(p => p === '/' || p.startsWith('/dashboard')),
    projects: isActive(p => p.startsWith('/projects') && p !== '/projects/smart-create'),
    myProjects: isActive(p => p.startsWith('/my-projects')),
    smartCreate: isActive(p => p === '/projects/smart-create'),
    chat: isActive(p => p === '/chat'),
  }
  return (
    <Box sx={{ minHeight: '100vh', bgcolor: theme.palette.background.default }}>
      <AppBar position="sticky" color="default">
        <Toolbar>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, flexGrow: 1, cursor: 'pointer' }} onClick={() => navigate('/') }>
            <Avatar src="/logo.png" alt="Plataforma Inteligente de Gestão de Iniciativas no MPSP" variant="square" sx={{ width: 28, height: 28, borderRadius: 0 }} />
            <Typography variant="h6" sx={{ fontWeight: 800, color: theme.palette.text.primary }}>Plataforma Inteligente de Gestão de Iniciativas no MPSP</Typography>
          </Box>
          {isSmall ? (
            <>
              <IconButton onClick={openMenu} color="primary"><MenuIcon/></IconButton>
              <Menu anchorEl={menuEl} open={Boolean(menuEl)} onClose={closeMenu} keepMounted>
                <MenuItem onClick={closeMenu} component={Link} to="/dashboard" selected={active.dashboard}>Dashboard</MenuItem>
                <MenuItem onClick={closeMenu} component={Link} to="/projects" selected={active.projects}>Iniciativas</MenuItem>
                <MenuItem onClick={closeMenu} component={Link} to="/my-projects" selected={active.myProjects}>Minhas Iniciativas</MenuItem>
                <Divider/>
                <MenuItem onClick={closeMenu} component={Link} to="/projects/smart-create" selected={active.smartCreate}>Criar com IA</MenuItem>
                <MenuItem onClick={closeMenu} component={Link} to="/chat" selected={active.chat}>Chat</MenuItem>
              </Menu>
            </>
          ) : (
            <>
              <Button color="primary" variant={active.dashboard ? 'contained' : 'text'} component={Link} to="/dashboard">Dashboard</Button>
              <Button color="primary" variant={active.projects ? 'contained' : 'text'} component={Link} to="/projects">Iniciativas</Button>
              <Button color="primary" variant={active.myProjects ? 'contained' : 'text'} component={Link} to="/my-projects">Minhas Iniciativas</Button>
              <Button color="primary" variant={active.smartCreate ? 'contained' : 'text'} component={Link} to="/projects/smart-create" sx={{ ml: 1 }}>Criar com IA</Button>
              <Button color="primary" variant={active.chat ? 'contained' : 'text'} component={Link} to="/chat">Chat</Button>
            </>
          )}
          {/* Processamentos removido temporariamente */}
        </Toolbar>
      </AppBar>
      <Box component="main" sx={{ width: '100%', py: { xs: 2, md: 3 }, px: { xs: 2, md: 6 } }}>
        {children}
      </Box>
    </Box>
  )
}
