import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Container,
  Avatar,
  Divider,
  Alert,
  Grid,
  Chip,
  Link as MuiLink
} from '@mui/material';
import {
  Microsoft as MicrosoftIcon,
  Security as SecurityIcon,
  Business as BusinessIcon
} from '@mui/icons-material';
import { useAuth } from '../hooks/useAuth';

const Login = () => {
  const { login, isLoading, error } = useAuth();

  const handleLogin = async () => {
    await login();
  };

  return (
    <Box sx={{ position: 'relative', minHeight: '100vh', overflow: 'hidden' }}>
      {/* Background mesh */}
      <Box
        sx={{
          position: 'absolute', inset: 0,
          background: `radial-gradient(1200px 600px at -10% -10%, rgba(0, 102, 204, 0.25), transparent 60%),
                      radial-gradient(900px 500px at 110% 10%, rgba(0, 200, 255, 0.22), transparent 55%),
                      linear-gradient(135deg, #0f172a 0%, #0b1020 100%)`,
        }}
      />
      {/* Soft glow overlay */}
      <Box sx={{ position: 'absolute', inset: 0, backdropFilter: 'blur(10px)', opacity: 0.35 }} />

      <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1, py: { xs: 6, md: 10 } }}>
        <Grid container spacing={6} alignItems="center">
          {/* Left: Hero copy */}
          <Grid item xs={12} md={7}>
            <Typography
              variant="h2"
              sx={{
                fontWeight: 800,
                lineHeight: 1.1,
                color: 'white',
                mb: 2,
              }}
            >
              Plataforma Inteligente de
              <Box component="span" sx={{ color: '#60a5fa' }}> Gestão</Box> e
              <Box component="span" sx={{ color: '#34d399' }}> Análise</Box> de Iniciativas
            </Typography>

            <Typography variant="h6" sx={{ color: 'rgba(255,255,255,0.8)', mb: 4 }}>
              Submeta, gerencie e conecte projetos a dados institucionais com automação por IA e governança.
            </Typography>

            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 5 }}>
              <Chip label="Login seguro Azure AD" color="primary" variant="outlined" sx={{ bgcolor: 'rgba(59,130,246,0.15)', color: '#93c5fd', borderColor: 'rgba(147,197,253,0.4)' }} />
              <Chip label="Integração institucional" color="success" variant="outlined" sx={{ bgcolor: 'rgba(16,185,129,0.12)', color: '#86efac', borderColor: 'rgba(134,239,172,0.4)' }} />
              <Chip label="RAG + LLM" variant="outlined" sx={{ bgcolor: 'rgba(250,250,250,0.08)', color: 'rgba(255,255,255,0.8)', borderColor: 'rgba(255,255,255,0.2)' }} />
            </Box>

            <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.6)' }}>
              Suporte: <MuiLink href="mailto:suporte@mp.sp.gov.br" sx={{ color: '#93c5fd' }}>suporte@mp.sp.gov.br</MuiLink>
            </Typography>
          </Grid>

          {/* Right: Sign-in card */}
          <Grid item xs={12} md={5}>
            <Card sx={{
              borderRadius: 4,
              bgcolor: 'rgba(17,24,39,0.7)',
              border: '1px solid rgba(255,255,255,0.08)',
              backdropFilter: 'blur(8px)',
              boxShadow: '0 20px 60px rgba(0,0,0,0.4)'
            }}>
              <Box sx={{ textAlign: 'center', pt: 4, px: 4 }}>
                <Avatar src="/logo.png" alt="Plataforma Inteligente de Gestão de Iniciativas no MPSP" sx={{ width: 72, height: 72, mx: 'auto', mb: 2, bgcolor: 'transparent' }} />
                <Typography variant="h5" sx={{ color: 'white', fontWeight: 800, textAlign: 'center' }}>Plataforma Inteligente de Gestão de Iniciativas no MPSP</Typography>
                <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)', mt: 1 }}>Use suas credenciais institucionais</Typography>
              </Box>

              <CardContent sx={{ p: 4 }}>
                {/* Error Alert */}
                {error && (
                  <Alert severity="error" sx={{ mb: 3 }}>
                    {error}
                  </Alert>
                )}

                <Button
                  fullWidth
                  variant="contained"
                  size="large"
                  onClick={handleLogin}
                  disabled={isLoading}
                  startIcon={<MicrosoftIcon />}
                  sx={{
                    py: 1.6,
                    fontSize: '1.06rem',
                    fontWeight: 700,
                    letterSpacing: 0.2,
                    background: 'linear-gradient(135deg, #2563eb 0%, #1e40af 100%)',
                    boxShadow: '0 10px 24px rgba(37,99,235,0.35)',
                    '&:hover': {
                      background: 'linear-gradient(135deg, #1d4ed8 0%, #1e3a8a 100%)',
                      boxShadow: '0 12px 28px rgba(37,99,235,0.45)'
                    },
                    '&:disabled': { background: '#334155' }
                  }}
                >
                  {isLoading ? 'Entrando...' : 'Entrar com Microsoft 365'}
                </Button>

                <Divider sx={{ my: 3, borderColor: 'rgba(255,255,255,0.08)' }} />

                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.6)' }}>
                    Ao fazer login, você concorda com os termos de uso e políticas de segurança.
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Box sx={{ textAlign: 'center', mt: 6 }}>
          <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
            © 2025 Ministério Público do Estado de São Paulo
          </Typography>
          <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.55)' }}>
            Desenvolvido pela Coordenadoria de Gestão Estratégica
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default Login;