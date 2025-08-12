import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  Grid,
  Chip,
  Divider,
  Alert,
  Link as MuiLink
} from '@mui/material';
import { ArrowBack, Edit, Delete, Download } from '@mui/icons-material';
import { getProject, listProjectAttachments, API_BASE_URL, projectService } from '../services/apiService';
import MembersTab from './project/MembersTab';
import LoadingSpinner from '../components/LoadingSpinner';
import { toast } from 'react-toastify';

/**
 * 👁️ Página de Visualização de Projeto
 * Exibe detalhes completos de um projeto
 */
const ProjectView = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  
  const [project, setProject] = useState(null);
  const [attachments, setAttachments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProject = async () => {
      try {
        setLoading(true);
        const data = await getProject(id);
        setProject(data);
        try {
          const atts = await listProjectAttachments(id);
          setAttachments(atts || []);
        } catch (e) {
          setAttachments([]);
        }
      } catch (err) {
        setError('Erro ao carregar projeto');
        console.error('Erro ao buscar projeto:', err);
        toast.error('Erro ao carregar projeto');
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchProject();
    }
  }, [id]);

  const handleEdit = () => {
    navigate(`/projects/${id}/edit`);
  };

  const handleDelete = async () => {
    if (window.confirm('Tem certeza que deseja excluir este projeto?')) {
      try {
        await projectService.delete(id);
        toast.success('Projeto excluído com sucesso!');
        navigate('/projects');
      } catch (err) {
        toast.error('Erro ao excluir projeto');
        console.error('Erro ao excluir projeto:', err);
      }
    }
  };

  if (loading) {
    return <LoadingSpinner message="Carregando projeto..." />;
  }

  if (error || !project) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="error">
          {error || 'Projeto não encontrado'}
        </Alert>
        <Box sx={{ mt: 2 }}>
          <Button
            variant="outlined"
            startIcon={<ArrowBack />}
            onClick={() => navigate('/projects')}
          >
            Voltar para Projetos
          </Button>
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth={false} sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 1 }}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            📄 {project.nome_da_iniciativa || project.nome_iniciativa || 'Projeto'}
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
            { (project.tipo_de_iniciativa || project.tipo_iniciativa) && (
              <Chip label={project.tipo_de_iniciativa || project.tipo_iniciativa} color="primary" size="small" />
            )}
            {project.classificacao && (
              <Chip label={project.classificacao} color="secondary" size="small" />
            )}
            { (project.fase_de_implementacao || project.fase) && (
              <Chip label={project.fase_de_implementacao || project.fase} color="success" size="small" />
            )}
          </Box>
        </Box>
        
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="outlined"
            startIcon={<ArrowBack />}
            onClick={() => navigate('/projects')}
          >
            Voltar
          </Button>
          <Button
            variant="contained"
            startIcon={<Edit />}
            onClick={handleEdit}
          >
            Editar
          </Button>
          <Button
            variant="outlined"
            color="error"
            startIcon={<Delete />}
            onClick={handleDelete}
          >
            Excluir
          </Button>
        </Box>
      </Box>

      {/* Conteúdo */}
      <Paper sx={{ p: { xs: 2, md: 3 } }}>
        <Grid container spacing={{ xs: 2, md: 3 }}>
          {/* Anexos */}
          {attachments && attachments.length > 0 && (
            <>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom color="primary" sx={{ mt: 3 }}>
                  📎 Anexos
                </Typography>
                   <Divider sx={{ mb: 2, borderColor: 'rgba(255,255,255,0.08)' }} />
              </Grid>
              <Grid item xs={12}>
                {attachments.map((a, idx) => {
                  const downloadUrl = `${API_BASE_URL}/projects/${id}/attachments/${a.id}/download`;
                  return (
                    <Box key={idx} sx={{ mb: 1, display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
                      <MuiLink href={a.stored_path} target="_blank" rel="noopener" sx={{ wordBreak: 'break-all' }}>
                        {a.original_name || a.stored_path}
                      </MuiLink>
                      <Button
                        variant="text"
                        size="small"
                        startIcon={<Download />}
                        component="a"
                        href={downloadUrl}
                      >
                        Baixar
                      </Button>
                      {typeof a.size_bytes === 'number' && (
                        <Typography variant="caption" color="text.secondary">
                          {(a.size_bytes / 1024).toFixed(1)} KB
                        </Typography>
                      )}
                    </Box>
                  );
                })}
              </Grid>
            </>
          )}
          {/* Informações Básicas */}
          <Grid item xs={12}>
            <Typography variant="h6" gutterBottom color="primary">
              📋 Informações Básicas
            </Typography>
            <Divider sx={{ mb: 2 }} />
          </Grid>

          {project.descricao && (
            <Grid item xs={12}>
              <Typography variant="subtitle2" gutterBottom>
                <strong>Descrição:</strong>
              </Typography>
              <Typography variant="body1" paragraph>
                {project.descricao}
              </Typography>
            </Grid>
          )}

          {project.objetivos && (
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" gutterBottom>
                <strong>Objetivos:</strong>
              </Typography>
              <Typography variant="body2">
                {project.objetivos}
              </Typography>
            </Grid>
          )}

          {project.beneficios_esperados && (
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" gutterBottom>
                <strong>Benefícios Esperados:</strong>
              </Typography>
              <Typography variant="body2">
                {project.beneficios_esperados}
              </Typography>
            </Grid>
          )}

          {/* Recursos e Gestão */}
          {(project.responsavel || project.departamento || project.recursos_necessarios) && (
            <>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom color="primary" sx={{ mt: 3 }}>
                  👥 Gestão e Recursos
                </Typography>
                <Divider sx={{ mb: 2 }} />
              </Grid>

              {project.responsavel && (
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" gutterBottom>
                    <strong>Responsável:</strong>
                  </Typography>
                  <Typography variant="body2">
                    {project.responsavel}
                  </Typography>
                </Grid>
              )}

              {project.departamento && (
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" gutterBottom>
                    <strong>Departamento:</strong>
                  </Typography>
                  <Typography variant="body2">
                    {project.departamento}
                  </Typography>
                </Grid>
              )}

              {project.recursos_necessarios && (
                <Grid item xs={12}>
                  <Typography variant="subtitle2" gutterBottom>
                    <strong>Recursos Necessários:</strong>
                  </Typography>
                  <Typography variant="body2">
                    {project.recursos_necessarios}
                  </Typography>
                </Grid>
              )}
            </>
          )}

          {/* Timeline e Orçamento */}
          {(project.cronograma || project.orcamento_estimado) && (
            <>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom color="primary" sx={{ mt: 3 }}>
                  📅 Timeline e Orçamento
                </Typography>
                <Divider sx={{ mb: 2 }} />
              </Grid>

              {project.cronograma && (
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" gutterBottom>
                    <strong>Cronograma:</strong>
                  </Typography>
                  <Typography variant="body2">
                    {project.cronograma}
                  </Typography>
                </Grid>
              )}

              {project.orcamento_estimado && (
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" gutterBottom>
                    <strong>Orçamento Estimado:</strong>
                  </Typography>
                  <Typography variant="body2">
                    {project.orcamento_estimado}
                  </Typography>
                </Grid>
              )}
            </>
          )}

          {/* Metadados */}
          <Grid item xs={12}>
            <Typography variant="h6" gutterBottom color="primary" sx={{ mt: 3 }}>
              ℹ️ Informações do Sistema
            </Typography>
            <Divider sx={{ mb: 2 }} />
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2" gutterBottom>
              <strong>ID do Projeto:</strong>
            </Typography>
            <Typography variant="body2">
              {project.id || project.project_id}
            </Typography>
          </Grid>

          {project.created_at && (
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" gutterBottom>
                <strong>Criado em:</strong>
              </Typography>
              <Typography variant="body2">
                {new Date(project.created_at).toLocaleString('pt-BR')}
              </Typography>
            </Grid>
          )}

          {project.updated_at && (
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" gutterBottom>
                <strong>Última atualização:</strong>
              </Typography>
              <Typography variant="body2">
                {new Date(project.updated_at).toLocaleString('pt-BR')}
              </Typography>
            </Grid>
          )}
        </Grid>
      </Paper>

      {/* Equipe do Projeto */}
      <Box sx={{ mt: 3 }}>
        <MembersTab projectId={id} />
      </Box>
    </Container>
  );
};

export default ProjectView;