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
  Alert
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
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 2
      }}
    >
      <Container maxWidth="sm">
        <Card
          sx={{
            borderRadius: 3,
            boxShadow: '0 20px 40px rgba(0,0,0,0.15)',
            overflow: 'hidden'
          }}
        >
          {/* Header */}
          <Box
            sx={{
              background: 'linear-gradient(135deg, #1976d2 0%, #1565c0 100%)',
              color: 'white',
              textAlign: 'center',
              py: 4,
              px: 3
            }}
          >
            <Avatar
              sx={{
                bgcolor: 'rgba(255,255,255,0.2)',
                width: 80,
                height: 80,
                mx: 'auto',
                mb: 2,
                fontSize: '2rem'
              }}
            >
              🤖
            </Avatar>
            <Typography variant="h4" component="h1" fontWeight="bold" gutterBottom>
              MCP - Sistema de IA
            </Typography>
            <Typography variant="subtitle1" sx={{ opacity: 0.9 }}>
              Análise Inteligente de Documentos
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.8, mt: 1 }}>
              Ministério Público do Estado de São Paulo
            </Typography>
          </Box>

          <CardContent sx={{ p: 4 }}>
            {/* Informações do Sistema */}
            <Box sx={{ mb: 4 }}>
              <Typography variant="h6" gutterBottom color="primary" fontWeight="500">
                Acesso Seguro via Microsoft 365
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Faça login com sua conta institucional do Ministério Público para acessar
                o sistema de análise de documentos com inteligência artificial.
              </Typography>

              {/* Features */}
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mb: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <SecurityIcon color="primary" />
                  <Typography variant="body2">
                    Autenticação segura via Azure Active Directory
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <BusinessIcon color="primary" />
                  <Typography variant="body2">
                    Acesso restrito a funcionários autorizados do MP
                  </Typography>
                </Box>
              </Box>
            </Box>

            <Divider sx={{ my: 3 }} />

            {/* Error Alert */}
            {error && (
              <Alert severity="error" sx={{ mb: 3 }}>
                {error}
              </Alert>
            )}

            {/* Login Button */}
            <Button
              fullWidth
              variant="contained"
              size="large"
              onClick={handleLogin}
              disabled={isLoading}
              startIcon={<MicrosoftIcon />}
              sx={{
                py: 1.5,
                fontSize: '1.1rem',
                fontWeight: 600,
                background: 'linear-gradient(135deg, #0078d4 0%, #106ebe 100%)',
                '&:hover': {
                  background: 'linear-gradient(135deg, #106ebe 0%, #005a9e 100%)',
                },
                '&:disabled': {
                  background: '#ccc',
                }
              }}
            >
              {isLoading ? 'Entrando...' : 'Entrar com Microsoft 365'}
            </Button>

            {/* Footer Info */}
            <Box sx={{ mt: 4, textAlign: 'center' }}>
              <Typography variant="caption" color="text.secondary">
                Ao fazer login, você concorda com os termos de uso do sistema.
              </Typography>
              <br />
              <Typography variant="caption" color="text.secondary">
                Para suporte técnico, entre em contato com a equipe de TI.
              </Typography>
            </Box>
          </CardContent>
        </Card>

        {/* Footer */}
        <Box sx={{ textAlign: 'center', mt: 3 }}>
          <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)' }}>
            © 2024 Ministério Público do Estado de São Paulo
          </Typography>
          <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.6)' }}>
            Desenvolvido pela Coordenadoria de Gestão Estratégica
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default Login;