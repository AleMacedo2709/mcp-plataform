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
  Fab,
  CardActionArea
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
import CardMedia from '@mui/material/CardMedia';
import { useTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { toast } from 'react-toastify';

import { projectService } from '../services/apiService';
import { useAuth } from '../hooks/useAuth';
import LoadingSpinner from '../components/LoadingSpinner';

const ProjectList = () => {
  const navigate = useNavigate();
  const theme = useTheme();
  const isXs = useMediaQuery(theme.breakpoints.down('sm'));
  const isSm = useMediaQuery(theme.breakpoints.down('md'));
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
    fase: '',
    unidade_gestora: '',
    selo: ''
  });
  const [deleteDialog, setDeleteDialog] = useState({ open: false, project: null });
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedProject, setSelectedProject] = useState(null);

  // Opções para filtros
  const tipoOptions = ['Boa Prática', 'Iniciativa', 'Programa'];
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
      const mapped = (response.projects || []).map(p => ({
        ...p,
        nome_iniciativa: p.nome_da_iniciativa || p.nome_iniciativa,
        tipo_iniciativa: p.tipo_de_iniciativa || p.tipo_iniciativa,
        fase: p.fase_de_implementacao || p.fase_implementacao || p.fase,
        data_inicial_operacao: p.data_inicial_de_operacao || p.data_inicial_operacao
      }))
      // opcional: buscar likes por projeto em paralelo (leve)
      try {
        const likesResults = await Promise.all(mapped.map(async (p)=> {
          try { const res = await fetch(`${API_BASE_URL}/projects/${p.id}/likes`); const d = await res.json(); return { id:p.id, likes: d.likes||0 } } catch { return { id:p.id, likes:0 } }
        }))
        const idToLikes = Object.fromEntries(likesResults.map(x=> [x.id, x.likes]))
        setProjects(mapped.map(p=> ({...p, likes: idToLikes[p.id] || 0})))
      } catch {
        setProjects(mapped)
      }
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
      field: 'unidade_gestora',
      headerName: 'Unidade Gestora',
      width: 180,
      hide: false,
    },
    {
      field: 'selo',
      headerName: 'Selo',
      width: 120,
      renderCell: (params) => (
        <Chip label={params.value || '-'} size="small" variant="outlined" />
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
      width: 130,
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
      width: 140,
      renderCell: (params) => {
        if (!params.value) return '-';
        try {
          return format(new Date(params.value), 'dd/MM/yyyy', { locale: ptBR });
        } catch {
          return '-';
        }
      }
    },
    // coluna de menu removida; clique na linha abre detalhes
  ];

  if (loading && projects.length === 0) {
    return <LoadingSpinner />;
  }

  const asCards = true;

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom sx={{ color: 'text.primary', fontWeight: 800 }}>
            Iniciativas Cadastradas
          </Typography>
          <Typography variant="body2" sx={{ color: 'text.secondary' }}>
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
            Nova Iniciativa
          </Button>
        )}
      </Box>

      {/* Filtros e Busca */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} sm={6} md={4}>
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
                sx={{
                  '& .MuiOutlinedInput-root': {
                    bgcolor: 'rgba(255,255,255,0.04)'
                  },
                  '& input::placeholder': { color: 'rgba(229,231,235,0.7)' }
                }}
              />
            </Grid>
            
            <Grid item xs={6} sm={3} md={2}>
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

            <Grid item xs={6} sm={3} md={2}>
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

            <Grid item xs={6} sm={3} md={2}>
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

            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                size="small"
                label="Unidade Gestora"
                value={filters.unidade_gestora}
                onChange={(e)=> setFilters(prev=> ({...prev, unidade_gestora: e.target.value}))}
              />
            </Grid>

            <Grid item xs={6} sm={3} md={2}>
              <FormControl fullWidth size="small">
                <InputLabel>Selo</InputLabel>
                <Select
                  value={filters.selo}
                  label="Selo"
                  onChange={(e) => setFilters(prev => ({ ...prev, selo: e.target.value }))}
                >
                  <MenuItem value="">Todos</MenuItem>
                  <MenuItem value="PGJ">PGJ</MenuItem>
                  <MenuItem value="CG Cidadã">CG Cidadã</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} sm={3} md={2}>
              <Button fullWidth variant="contained" color="primary"
                startIcon={<FilterIcon />}
                onClick={() => { setSearch(''); setFilters({ tipo_iniciativa: '', classificacao: '', fase: '', unidade_gestora:'', selo:'' }); }}
                sx={{ fontWeight: 700 }}
              >Limpar</Button>
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

      {/* Cards Grid */}
      {asCards && (
        <Grid container spacing={2}>
          {projects.map((p)=> {
            const likes = p.likes || p.total_likes || 0;
            return (
              <Grid item xs={12} sm={6} md={4} lg={3} key={p.id}>
                <Card sx={{ position:'relative' }}>
                  {/* Badge de curtidas */}
                  <Box sx={{ position:'absolute', top: 8, left: 8, bgcolor:'error.main', color:'#fff', px:1.2, py:0.3, borderRadius: 2, fontSize:12, fontWeight:700 }}>
                    {likes} curtidas
                  </Box>
                  <CardActionArea onClick={()=> navigate(`/projects/${p.id}`)}>
                    <CardMedia
                      component="img"
                      image={p.capa_da_iniciativa || '/logo.png'}
                      alt={p.nome_da_iniciativa}
                      sx={{ height: 140, objectFit:'contain', bgcolor:'#f5f7fb' }}
                    />
                    <CardContent>
                      <Typography variant="overline" sx={{ color:'text.secondary' }}>Título:</Typography>
                      <Typography variant="subtitle1" sx={{ fontWeight: 700 }} noWrap>
                        {p.nome_da_iniciativa}
                      </Typography>
                      <Typography variant="body2" sx={{ color:'text.secondary' }} noWrap>
                        {p.unidade_gestora || '-'} {p.selo ? `• ${p.selo}` : ''}
                      </Typography>
                      <Box sx={{ mt: 1, display:'flex', gap: 0.5, flexWrap:'wrap' }}>
                        {p.tipo_de_iniciativa && <Chip size="small" label={p.tipo_de_iniciativa} />}
                        {p.classificacao && <Chip size="small" color="secondary" label={p.classificacao} />}
                        {p.fase && <Chip size="small" color={getStatusColor(p.fase)} label={p.fase} />}
                      </Box>
                    </CardContent>
                  </CardActionArea>
                </Card>
              </Grid>
            )
          })}
        </Grid>
      )}

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