import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Chip,
  Button
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Folder as FolderIcon,
  Upload as UploadIcon,
  Analytics as AnalyticsIcon,
  Add as AddIcon,
  Refresh as RefreshIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';

import { projectService, reportService } from '../services/apiService';
import { useAuth } from '../hooks/useAuth';
import LoadingSpinner from '../components/LoadingSpinner';

const Dashboard = () => {
  const navigate = useNavigate();
  const { user, hasPermission } = useAuth();
  const [stats, setStats] = useState(null);
  const [recentProjects, setRecentProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Carregar estatísticas
      const statsResponse = await reportService.dashboard();
      setStats(statsResponse);

      // Carregar projetos recentes
      const projectsResponse = await projectService.list({ 
        limit: 5, 
        orderBy: 'created_at',
        order: 'desc' 
      });
      setRecentProjects(projectsResponse.projects || []);

    } catch (error) {
      console.error('Erro ao carregar dashboard:', error);
      toast.error('Erro ao carregar dados do dashboard');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (fase) => {
    switch (fase) {
      case 'Implementação integral':
        return 'success';
      case 'Implementação parcial':
        return 'warning';
      default:
        return 'default';
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 800 }}>
            Dashboard
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Bem-vindo de volta, {user?.name?.split(' ')[0]}! 
          </Typography>
        </Box>
        
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button variant="outlined" startIcon={<RefreshIcon />} onClick={loadDashboardData}>
            Atualizar
          </Button>
          
          {hasPermission('user') && (
            <Button variant="contained" startIcon={<AddIcon />} onClick={() => navigate('/projects/new')}>
              Novo Projeto
            </Button>
          )}
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* Cards de Estatísticas */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography color="textSecondary" gutterBottom variant="overline">
                    Total de Projetos
                  </Typography>
                  <Typography variant="h4" component="h2">
                    {stats?.totalProjects || 0}
                  </Typography>
                </Box>
                <Avatar sx={{ bgcolor: 'primary.main' }}>
                  <FolderIcon />
                </Avatar>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography color="textSecondary" gutterBottom variant="overline">
                    Em Andamento
                  </Typography>
                  <Typography variant="h4" component="h2">
                    {stats?.projectsInProgress || 0}
                  </Typography>
                </Box>
                <Avatar sx={{ bgcolor: 'warning.main' }}>
                  <TrendingUpIcon />
                </Avatar>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography color="textSecondary" gutterBottom variant="overline">
                    Concluídos
                  </Typography>
                  <Typography variant="h4" component="h2">
                    {stats?.projectsCompleted || 0}
                  </Typography>
                </Box>
                <Avatar sx={{ bgcolor: 'success.main' }}>
                  <AnalyticsIcon />
                </Avatar>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography color="textSecondary" gutterBottom variant="overline">
                    Documentos Processados
                  </Typography>
                  <Typography variant="h4" component="h2">
                    {stats?.documentsProcessed || 0}
                  </Typography>
                </Box>
                <Avatar sx={{ bgcolor: 'info.main' }}>
                  <UploadIcon />
                </Avatar>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Projetos Recentes */}
        <Grid item xs={12} md={12}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">
                  Projetos Recentes
                </Typography>
                <Button
                  size="small"
                  onClick={() => navigate('/projects')}
                >
                  Ver todos
                </Button>
              </Box>
              
              <List>
                {recentProjects.length > 0 ? recentProjects.map((project) => (
                  <ListItem
                    key={project.id}
                    button
                    onClick={() => navigate(`/projects/${project.id}`)}
                    sx={{ 
                      borderRadius: 1,
                      mb: 1,
                      '&:hover': {
                        backgroundColor: 'action.hover',
                      }
                    }}
                  >
                    <ListItemAvatar>
                      <Avatar sx={{ bgcolor: 'primary.light' }}>
                        <FolderIcon />
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={
                        <Typography variant="subtitle2" noWrap>
                          {project.nome_iniciativa}
                        </Typography>
                      }
                      secondary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 0.5 }}>
                          <Chip 
                            label={project.fase} 
                            size="small"
                            color={getStatusColor(project.fase)}
                          />
                          <Typography variant="caption" color="text.secondary">
                            {project.tipo_iniciativa}
                          </Typography>
                        </Box>
                      }
                    />
                  </ListItem>
                )) : (
                  <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 2 }}>
                    Nenhum projeto encontrado
                  </Typography>
                )}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Ações Rápidas */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Ações Rápidas
              </Typography>
              
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <Button
                  variant="outlined"
                  startIcon={<AddIcon />}
                  onClick={() => navigate('/projects/new')}
                  disabled={!hasPermission('user')}
                >
                  Criar Projeto
                </Button>
                
                <Button variant="outlined" startIcon={<UploadIcon />} onClick={() => navigate('/projects/smart-create')}>
                  Analisar Documento
                </Button>
                
                <Button variant="outlined" startIcon={<FolderIcon />} onClick={() => navigate('/projects')}>
                  Ver Todos os Projetos
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;