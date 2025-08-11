import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  Avatar,
  Grid,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip
} from '@mui/material';
import { 
  ArrowBack, 
  Person, 
  Email, 
  Business, 
  AdminPanelSettings,
  ExitToApp
} from '@mui/icons-material';
import { useMsal } from '@azure/msal-react';
import { toast } from 'react-toastify';

/**
 * 👤 Página de Perfil do Usuário
 * Exibe informações do usuário logado via Azure AD
 */
const Profile = () => {
  const navigate = useNavigate();
  const { instance, accounts } = useMsal();
  const [userInfo, setUserInfo] = useState(null);

  useEffect(() => {
    if (accounts && accounts.length > 0) {
      const account = accounts[0];
      setUserInfo({
        name: account.name || 'Usuário',
        email: account.username || 'email@example.com',
        roles: ['Usuário'], // Roles podem vir de claims do token
        department: 'Ministério Público',
        lastLogin: new Date().toLocaleDateString('pt-BR')
      });
    }
  }, [accounts]);

  const handleLogout = async () => {
    try {
      await instance.logoutPopup();
      toast.success('Logout realizado com sucesso!');
      navigate('/');
    } catch (error) {
      console.error('Erro no logout:', error);
      toast.error('Erro ao fazer logout');
    }
  };

  const getUserInitials = (name) => {
    if (!name) return 'U';
    return name
      .split(' ')
      .map(word => word[0])
      .join('')
      .substring(0, 2)
      .toUpperCase();
  };

  if (!userInfo) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Typography>Carregando perfil...</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1">
          Meu Perfil
        </Typography>
        
        <Button
          variant="outlined"
          startIcon={<ArrowBack />}
          onClick={() => navigate('/dashboard')}
        >
          Voltar
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* Informações Básicas */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Avatar
              sx={{ 
                width: 120, 
                height: 120, 
                margin: '0 auto 16px',
                bgcolor: 'primary.main',
                fontSize: '2rem'
              }}
            >
              {getUserInitials(userInfo.name)}
            </Avatar>
            
            <Typography variant="h5" gutterBottom>
              {userInfo.name}
            </Typography>
            
            <Typography variant="body2" color="text.secondary" gutterBottom>
              {userInfo.email}
            </Typography>
            
            <Box sx={{ mt: 2 }}>
              {userInfo.roles.map((role, index) => (
                <Chip
                  key={index}
                  label={role}
                  color="primary"
                  size="small"
                  sx={{ mr: 1, mb: 1 }}
                />
              ))}
            </Box>

            <Button
              variant="contained"
              color="error"
              startIcon={<ExitToApp />}
              onClick={handleLogout}
              sx={{ mt: 3 }}
              fullWidth
            >
              Sair do Sistema
            </Button>
          </Paper>
        </Grid>

        {/* Detalhes */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Informações da Conta
            </Typography>
            
            <List>
              <ListItem>
                <ListItemIcon>
                  <Person />
                </ListItemIcon>
                <ListItemText
                  primary="Nome Completo"
                  secondary={userInfo.name}
                />
              </ListItem>
              
              <Divider variant="inset" component="li" />
              
              <ListItem>
                <ListItemIcon>
                  <Email />
                </ListItemIcon>
                <ListItemText
                  primary="Email"
                  secondary={userInfo.email}
                />
              </ListItem>
              
              <Divider variant="inset" component="li" />
              
              <ListItem>
                <ListItemIcon>
                  <Business />
                </ListItemIcon>
                <ListItemText
                  primary="Departamento"
                  secondary={userInfo.department}
                />
              </ListItem>
              
              <Divider variant="inset" component="li" />
              
              <ListItem>
                <ListItemIcon>
                  <AdminPanelSettings />
                </ListItemIcon>
                <ListItemText
                  primary="Permissões"
                  secondary={userInfo.roles.join(', ')}
                />
              </ListItem>
            </List>

            <Divider sx={{ my: 3 }} />

            <Typography variant="h6" gutterBottom>
              Informações de Sessão
            </Typography>
            
            <Typography variant="body2" color="text.secondary">
              Último acesso: {userInfo.lastLogin}
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Profile;