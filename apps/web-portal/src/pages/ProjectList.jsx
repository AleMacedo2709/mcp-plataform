import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  IconButton,
  Chip,
  TextField,
  InputAdornment,
  Grid,
  Menu,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Alert,
  Pagination,
  FormControl,
  InputLabel,
  Select,
  Tooltip,
  Fab
} from '@mui/material';
import {
  Search as SearchIcon,
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  MoreVert as MoreVertIcon,
  FilterList as FilterIcon,
  FileDownload as DownloadIcon
} from '@mui/icons-material';
import { DataGrid } from '@mui/x-data-grid';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { toast } from 'react-toastify';

import { projectService } from '../services/apiService';
import { useAuth } from '../hooks/useAuth';
import LoadingSpinner from '../components/LoadingSpinner';

const ProjectList = () => {
  const navigate = useNavigate();
  const { user, hasPermission } = useAuth();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(0);
  const [pageSize, setPageSize] = useState(10);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState('');
  const [filters, setFilters] = useState({
    ownerMe: false,
    tipo_iniciativa: '',
    classificacao: '',
    fase: ''
  });
  const [deleteDialog, setDeleteDialog] = useState({ open: false, project: null });
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedProject, setSelectedProject] = useState(null);

  // Opções para filtros
  const tipoOptions = ['Boa Prática', 'Projeto', 'Programa'];
  const classificacaoOptions = ['Ação', 'Campanha', 'Ferramenta'];
  const faseOptions = ['Implementação parcial', 'Implementação integral'];

  useEffect(() => {
    loadProjects();
  }, [page, pageSize, search, filters]);

  const loadProjects = async () => {
    try {
      setLoading(true);
      const params = {
        skip: page * pageSize,
        limit: pageSize,
        search: search || undefined,
        ...filters
      };

      const response = await projectService.getAll(params);
      setProjects(response.projects || []);
      setTotal(response.total || 0);
      setError(null);
    } catch (err) {
      console.error('Erro ao carregar projetos:', err);
      setError('Erro ao carregar projetos');
      toast.error('Erro ao carregar projetos');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (project) => {
    try {
      await projectService.delete(project.id);
      toast.success('Projeto removido com sucesso!');
      loadProjects();
      setDeleteDialog({ open: false, project: null });
    } catch (err) {
      console.error('Erro ao remover projeto:', err);
      toast.error('Erro ao remover projeto');
    }
  };

  const handleMenuClick = (event, project) => {
    setAnchorEl(event.currentTarget);
    setSelectedProject(project);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setSelectedProject(null);
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

  const columns = [
    {
      field: 'nome_iniciativa',
      headerName: 'Nome da Iniciativa',
      flex: 1,
      minWidth: 250,
      renderCell: (params) => (
        <Box>
          <Typography variant="body2" fontWeight="500" noWrap>
            {params.value}
          </Typography>
          <Typography variant="caption" color="text.secondary" noWrap>
            ID: {params.row.id}
          </Typography>
        </Box>
      )
    },
    {
      field: 'tipo_iniciativa',
      headerName: 'Tipo',
      width: 120,
      renderCell: (params) => (
        <Chip 
          label={params.value} 
          size="small" 
          variant="outlined"
          color="primary"
        />
      )
    },
    {
      field: 'classificacao',
      headerName: 'Classificação',
      width: 130,
      renderCell: (params) => (
        <Chip 
          label={params.value} 
          size="small" 
          variant="filled"
          color="secondary"
        />
      )
    },
    {
      field: 'fase',
      headerName: 'Status',
      width: 150,
      renderCell: (params) => (
        <Chip 
          label={params.value} 
          size="small"
          color={getStatusColor(params.value)}
        />
      )
    },
    {
      field: 'data_inicial_operacao',
      headerName: 'Data Inicial',
      width: 120,
      renderCell: (params) => {
        if (!params.value) return '-';
        try {
          return format(new Date(params.value), 'dd/MM/yyyy', { locale: ptBR });
        } catch {
          return params.value;
        }
      }
    },
    {
      field: 'created_at',
      headerName: 'Criado em',
      width: 120,
      renderCell: (params) => {
        if (!params.value) return '-';
        try {
          return format(new Date(params.value), 'dd/MM/yyyy', { locale: ptBR });
        } catch {
          return '-';
        }
      }
    },
    {
      field: 'actions',
      headerName: 'Ações',
      width: 100,
      sortable: false,
      filterable: false,
      renderCell: (params) => (
        <Box>
          <Tooltip title="Mais opções">
            <IconButton
              size="small"
              onClick={(e) => handleMenuClick(e, params.row)}
            >
              <MoreVertIcon />
            </IconButton>
          </Tooltip>
        </Box>
      )
    }
  ];

  if (loading && projects.length === 0) {
    return <LoadingSpinner />;
  }

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Projetos Cadastrados
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Gerencie todos os projetos do sistema
          </Typography>
        </Box>
        
        {hasPermission('user') && (
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => navigate('/projects/new')}
            sx={{ borderRadius: 2 }}
          >
            Novo Projeto
          </Button>
        )}
      </Box>

      {/* Filtros e Busca */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={3} alignItems="center">
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                placeholder="Buscar projetos..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
            
            <Grid item xs={12} md={2}>
              <FormControl fullWidth size="small">
                <InputLabel>Tipo</InputLabel>
                <Select
                  value={filters.tipo_iniciativa}
                  label="Tipo"
                  onChange={(e) => setFilters(prev => ({ ...prev, tipo_iniciativa: e.target.value }))}
                >
                  <MenuItem value="">Todos</MenuItem>
                  {tipoOptions.map(option => (
                    <MenuItem key={option} value={option}>{option}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} md={2}>
              <FormControl fullWidth size="small">
                <InputLabel>Classificação</InputLabel>
                <Select
                  value={filters.classificacao}
                  label="Classificação"
                  onChange={(e) => setFilters(prev => ({ ...prev, classificacao: e.target.value }))}
                >
                  <MenuItem value="">Todas</MenuItem>
                  {classificacaoOptions.map(option => (
                    <MenuItem key={option} value={option}>{option}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} md={2}>
              <FormControl fullWidth size="small">
                <InputLabel>Status</InputLabel>
                <Select
                  value={filters.fase}
                  label="Status"
                  onChange={(e) => setFilters(prev => ({ ...prev, fase: e.target.value }))}
                >
                  <MenuItem value="">Todos</MenuItem>
                  {faseOptions.map(option => (
                    <MenuItem key={option} value={option}>{option}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} md={2}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<FilterIcon />}
                onClick={() => {
                  setSearch('');
                  setFilters({ tipo_iniciativa: '', classificacao: '', fase: '' });
                }}
              >
                Limpar
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Error Alert */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Data Grid */}
      <Card>
        <Box sx={{ height: 600, width: '100%' }}>
          <DataGrid
            rows={projects}
            columns={columns}
            pageSize={pageSize}
            rowsPerPageOptions={[5, 10, 25, 50]}
            onPageSizeChange={(newPageSize) => setPageSize(newPageSize)}
            page={page}
            onPageChange={(newPage) => setPage(newPage)}
            rowCount={total}
            paginationMode="server"
            loading={loading}
            disableSelectionOnClick
            localeText={{
              // Tradução para português
              noRowsLabel: 'Nenhum projeto encontrado',
              footerRowSelected: (count) => `${count} projeto(s) selecionado(s)`,
            }}
            sx={{
              border: 'none',
              '& .MuiDataGrid-cell': {
                borderBottom: '1px solid #f0f0f0',
              },
              '& .MuiDataGrid-columnHeaders': {
                backgroundColor: '#f8f9fa',
                borderBottom: '2px solid #e9ecef',
              },
            }}
          />
        </Box>
      </Card>

      {/* Menu de Ações */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={() => {
          navigate(`/projects/${selectedProject?.id}`);
          handleMenuClose();
        }}>
          <ViewIcon sx={{ mr: 1 }} />
          Visualizar
        </MenuItem>
        
        {hasPermission('user') && (
          <MenuItem onClick={() => {
            navigate(`/projects/${selectedProject?.id}/edit`);
            handleMenuClose();
          }}>
            <EditIcon sx={{ mr: 1 }} />
            Editar
          </MenuItem>
        )}
        
        {hasPermission('admin') && (
          <MenuItem 
            onClick={() => {
              setDeleteDialog({ open: true, project: selectedProject });
              handleMenuClose();
            }}
            sx={{ color: 'error.main' }}
          >
            <DeleteIcon sx={{ mr: 1 }} />
            Remover
          </MenuItem>
        )}
      </Menu>

      {/* Dialog de Confirmação de Exclusão */}
      <Dialog
        open={deleteDialog.open}
        onClose={() => setDeleteDialog({ open: false, project: null })}
      >
        <DialogTitle>Confirmar Exclusão</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Tem certeza que deseja remover o projeto "{deleteDialog.project?.nome_iniciativa}"?
            Esta ação não pode ser desfeita.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialog({ open: false, project: null })}>
            Cancelar
          </Button>
          <Button 
            onClick={() => handleDelete(deleteDialog.project)} 
            color="error"
            variant="contained"
          >
            Remover
          </Button>
        </DialogActions>
      </Dialog>

      {/* FAB para adicionar projeto (mobile) */}
      {hasPermission('user') && (
        <Fab
          color="primary"
          aria-label="add"
          onClick={() => navigate('/projects/new')}
          sx={{
            position: 'fixed',
            bottom: 16,
            right: 16,
            display: { xs: 'flex', md: 'none' }
          }}
        >
          <AddIcon />
        </Fab>
      )}
    </Box>
  );
};

export default ProjectList;