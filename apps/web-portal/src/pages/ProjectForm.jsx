import React, {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; useState, useEffect } from 'react'
import {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; useLocation } from 'react-router-dom';
import {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; useParams, useNavigate } from 'react-router-dom';
import {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
  Container,
  Paper,
  Typography,
  Box,
  Button,
  TextField,
  Grid,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Divider
} from '@mui/material';
import {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; ArrowBack, Save } from '@mui/icons-material';
import {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; getProject, updateProject, createProject } from '../services/apiService';
import LoadingSpinner from '../components/LoadingSpinner';
import {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; toast } from 'react-toastify';
import {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
  TIPOS_INICIATIVA,
  CLASSIFICACOES,
  FASES_IMPLEMENTACAO,
  CATEGORIAS,
  OBJETIVOS_ESTRATEGICOS,

  helpers
} from '../constants/formOptions';

/**
 * 📝 Formulário de Projeto CNMP 2025
 * Criação e edição de projetos com schema completo
 */
const ProjectForm = () => {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
  const {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; id } = useParams();
  const navigate = useNavigate();
  const isEdit = Boolean(id);
  
  const [formData, setFormData] = useState({
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
    // Campos obrigatórios Prêmio CNMP 2025
    nome_iniciativa: '',
    tipo_iniciativa: '',
    classificacao: '',
    natureza_iniciativa: '',
    iniciativa_vinculada: '',
    objetivo_estrategico_pen_mp: '',
    promocao_objetivo_estrategico: '',
    data_inicial_operacao: '',
    fase_implementacao: '',
    descricao: '',
    estimativa_recursos: '',
    publico_impactado: '',
    orgaos_envolvidos: '',
    contatos: '',
    desafio_1: '',
    desafio_2: '',
    desafio_3: '',
    resolutividade: '',
    inovacao: '',
    transparencia: '',
    proatividade: '',
    cooperacao: '',
    resultado_1: '',
    resultado_2: '',
    resultado_3: '',
    categoria: ''
  });
  
  const [loading, setLoading] = useState(isEdit);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
    const fetchProject = async () => {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
      try {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
        setLoading(true);
        const data = await getProject(id);
        setFormData({
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
          nome_iniciativa: data.nome_iniciativa || '',
          tipo_iniciativa: data.tipo_iniciativa || '',
          classificacao: data.classificacao || '',
          natureza_iniciativa: data.natureza_iniciativa || '',
          iniciativa_vinculada: data.iniciativa_vinculada || '',
          objetivo_estrategico_pen_mp: data.objetivo_estrategico_pen_mp || '',
          promocao_objetivo_estrategico: data.promocao_objetivo_estrategico || '',
          data_inicial_operacao: data.data_inicial_operacao || '',
          fase_implementacao: data.fase_implementacao || data.fase || '',
          descricao: data.descricao || '',
          estimativa_recursos: data.estimativa_recursos || '',
          publico_impactado: data.publico_impactado || '',
          orgaos_envolvidos: data.orgaos_envolvidos || '',
          contatos: data.contatos || '',
          desafio_1: data.desafio_1 || '',
          desafio_2: data.desafio_2 || '',
          desafio_3: data.desafio_3 || '',
          resolutividade: data.resolutividade || '',
          inovacao: data.inovacao || '',
          transparencia: data.transparencia || '',
          proatividade: data.proatividade || '',
          cooperacao: data.cooperacao || '',
          resultado_1: data.resultado_1 || '',
          resultado_2: data.resultado_2 || '',
          resultado_3: data.resultado_3 || '',
          categoria: data.categoria || ''
        });
      } catch (err) {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
        setError('Erro ao carregar projeto');
        console.error('Erro ao buscar projeto:', err);
      } finally {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
        setLoading(false);
      }
    };

    if (isEdit && id) {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
      fetchProject();
    }
  }, [id, isEdit]);

  const handleChange = (field) => (event) => {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
    setFormData({
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
      ...formData,
      [field]: event.target.value
    });
  };

  const handleSubmit = async (event) => {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
    event.preventDefault();
    
    // Validação básica
    if (!formData.nome_iniciativa.trim()) {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
      toast.error('Nome da iniciativa é obrigatório');
      return;
    }

    if (!formData.descricao.trim()) {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
      toast.error('Descrição é obrigatória');
      return;
    }

    try {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
      setSaving(true);
      
      if (isEdit) {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
        await updateProject(id, formData);
        toast.success('Projeto atualizado com sucesso!');
      } else {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
        await createProject(formData);
        toast.success('Projeto criado com sucesso!');
      }
      
      navigate('/projects');
    } catch (err) {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
      const errorMessage = isEdit 
        ? 'Erro ao atualizar projeto' 
        : 'Erro ao criar projeto';
      toast.error(errorMessage);
      console.error('Erro ao salvar projeto:', err);
    } finally {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
      setSaving(false);
    }
  };

  if (loading) {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
    return <LoadingSpinner message="Carregando projeto..." />;
  }

  if (error) {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;
    return (
      <Container maxWidth="lg" sx={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; mt: 4 }}>
        <Alert severity="error">
          {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;error}
        </Alert>
        <Box sx={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; mt: 2 }}>
          <Button
            variant="outlined"
            startIcon={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;<ArrowBack />}
            onClick={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;() => navigate('/projects')}
          >
            Voltar para Projetos
          </Button>
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; mt: 4, mb: 4 }}>
      {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;/* Header */}
      <Box sx={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1">
          {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;isEdit ? '✏️ Editar Projeto' : '➕ Novo Projeto'}
        </Typography>
        <Button
          variant="outlined"
          startIcon={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;<ArrowBack />}
          onClick={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;() => navigate('/projects')}
          disabled={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;saving}
        >
          Voltar
        </Button>
      </Box>

      <Paper sx={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; p: 4 }}>
        <form onSubmit={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleSubmit}>
          <Grid container spacing={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;3}>
            {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;/* SEÇÃO 1: IDENTIFICAÇÃO DA INICIATIVA */}
            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12}>
              <Typography variant="h6" gutterBottom sx={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; color: 'primary.main', fontWeight: 'bold' }}>
                📋 1. Identificação da Iniciativa
              </Typography>
              <Divider sx={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; mb: 2 }} />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12}>
              <TextField
                fullWidth
                label="Nome da Iniciativa *"
                value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.nome_iniciativa}
                onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('nome_iniciativa')}
                required
                inputProps={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; maxLength: 300 }}
                helperText={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;`${
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;helpers.getMensagemLimite('nome_iniciativa')} ${
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;!formData.nome_iniciativa && saving ? '- Campo obrigatório' : ''}`}
                error={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;!formData.nome_iniciativa && saving}
              />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12} md={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;4}>
              <FormControl fullWidth required>
                <InputLabel>Tipo de Iniciativa *</InputLabel>
                <Select
                  value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.tipo_iniciativa}
                  onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('tipo_iniciativa')}
                  label="Tipo de Iniciativa *"
                >
                  {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;TIPOS_INICIATIVA.map((tipo) => (
                    <MenuItem key={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;tipo} value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;tipo}>
                      {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;helpers.getIconeTipo(tipo)} {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;tipo}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12} md={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;4}>
              <FormControl fullWidth required>
                <InputLabel>Classificação *</InputLabel>
                <Select
                  value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.classificacao}
                  onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('classificacao')}
                  label="Classificação *"
                >
                  {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;CLASSIFICACOES.map((classificacao) => (
                    <MenuItem key={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;classificacao} value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;classificacao}>
                      {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;classificacao}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12} md={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;4}>
              <FormControl fullWidth required>
                <InputLabel>Categoria *</InputLabel>
                <Select
                  value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.categoria}
                  onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('categoria')}
                  label="Categoria *"
                >
                  {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;CATEGORIAS.map((categoria) => (
                    <MenuItem key={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;categoria} value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;categoria}>
                      {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;categoria}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12} md={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;6}>
              <TextField
                fullWidth
                label="Natureza da Iniciativa"
                value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.natureza_iniciativa}
                onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('natureza_iniciativa')}
                inputProps={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; maxLength: 100 }}
                helperText={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;helpers.getMensagemLimite('natureza_iniciativa')}
              />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12} md={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;6}>
              <TextField
                fullWidth
                label="Iniciativa Vinculada"
                value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.iniciativa_vinculada}
                onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('iniciativa_vinculada')}
                inputProps={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; maxLength: 300 }}
                helperText={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;helpers.getMensagemLimite('iniciativa_vinculada')}
              />
            </Grid>

            {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;/* SEÇÃO 2: ALINHAMENTO ESTRATÉGICO */}
            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12}>
              <Typography variant="h6" gutterBottom sx={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; color: 'primary.main', fontWeight: 'bold', mt: 3 }}>
                🎯 2. Alinhamento Estratégico PEN-MP
              </Typography>
              <Divider sx={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; mb: 2 }} />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12}>
              <FormControl fullWidth>
                <InputLabel>Objetivo Estratégico PEN-MP</InputLabel>
                <Select
                  value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.objetivo_estrategico_pen_mp}
                  onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('objetivo_estrategico_pen_mp')}
                  label="Objetivo Estratégico PEN-MP"
                >
                  {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;OBJETIVOS_ESTRATEGICOS.map((objetivo) => (
                    <MenuItem key={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;objetivo} value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;objetivo}>
                      {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;objetivo}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12} md={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;6}>
              <TextField
                fullWidth
                multiline
                rows={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;2}
                label="Promoção do Objetivo Estratégico"
                value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.promocao_objetivo_estrategico}
                onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('promocao_objetivo_estrategico')}
                inputProps={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; maxLength: 100 }}
                helperText={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;helpers.getMensagemLimite('promocao_objetivo_estrategico')}
              />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12} md={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;6}>
              <TextField
                fullWidth
                label="Data Inicial de Operação"
                value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.data_inicial_operacao}
                onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('data_inicial_operacao')}
                type="date"
                InputLabelProps={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; shrink: true }}
              />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12}>
              <FormControl fullWidth>
                <InputLabel>Fase de Implementação</InputLabel>
                <Select
                  value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.fase_implementacao}
                  onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('fase_implementacao')}
                  label="Fase de Implementação"
                >
                  {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;FASES_IMPLEMENTACAO.map((fase) => (
                    <MenuItem key={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;fase} value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;fase}>
                      {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;fase}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;/* SEÇÃO 3: DESCRIÇÃO DETALHADA */}
            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12}>
              <Typography variant="h6" gutterBottom sx={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; color: 'primary.main', fontWeight: 'bold', mt: 3 }}>
                📝 3. Descrição da Iniciativa
              </Typography>
              <Divider sx={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; mb: 2 }} />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12}>
              <TextField
                fullWidth
                multiline
                rows={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;5}
                label="Descrição Detalhada *"
                value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.descricao}
                onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('descricao')}
                required
                inputProps={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; maxLength: 1000 }}
                helperText={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;helpers.getMensagemLimite('descricao')}
                error={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;!formData.descricao && saving}
              />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12} md={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;6}>
              <TextField
                fullWidth
                multiline
                rows={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;2}
                label="Estimativa de Recursos"
                value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.estimativa_recursos}
                onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('estimativa_recursos')}
                inputProps={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; maxLength: 200 }}
                helperText={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;helpers.getMensagemLimite('estimativa_recursos')}
              />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12} md={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;6}>
              <TextField
                fullWidth
                label="Público Impactado"
                value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.publico_impactado}
                onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('publico_impactado')}
                inputProps={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; maxLength: 100 }}
                helperText={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;helpers.getMensagemLimite('publico_impactado')}
              />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12} md={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;6}>
              <TextField
                fullWidth
                multiline
                rows={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;2}
                label="Órgãos Envolvidos"
                value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.orgaos_envolvidos}
                onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('orgaos_envolvidos')}
                inputProps={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; maxLength: 300 }}
                helperText={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;helpers.getMensagemLimite('orgaos_envolvidos')}
              />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12} md={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;6}>
              <TextField
                fullWidth
                multiline
                rows={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;2}
                label="Contatos"
                value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.contatos}
                onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('contatos')}
                inputProps={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; maxLength: 300 }}
                helperText={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;helpers.getMensagemLimite('contatos')}
              />
            </Grid>

            {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;/* SEÇÃO 4: DESAFIOS */}
            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12}>
              <Typography variant="h6" gutterBottom sx={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; color: 'primary.main', fontWeight: 'bold', mt: 3 }}>
                ⚡ 4. Desafios Enfrentados
              </Typography>
              <Divider sx={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; mb: 2 }} />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12} md={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;4}>
              <TextField
                fullWidth
                label="Desafio 1"
                value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.desafio_1}
                onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('desafio_1')}
                inputProps={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; maxLength: 100 }}
                helperText={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;helpers.getMensagemLimite('desafio_1')}
              />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12} md={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;4}>
              <TextField
                fullWidth
                label="Desafio 2"
                value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.desafio_2}
                onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('desafio_2')}
                inputProps={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; maxLength: 100 }}
                helperText={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;helpers.getMensagemLimite('desafio_2')}
              />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12} md={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;4}>
              <TextField
                fullWidth
                label="Desafio 3"
                value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.desafio_3}
                onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('desafio_3')}
                inputProps={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; maxLength: 100 }}
                helperText={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;helpers.getMensagemLimite('desafio_3')}
              />
            </Grid>

            {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;/* SEÇÃO 5: CRITÉRIOS DE AVALIAÇÃO */}
            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12}>
              <Typography variant="h6" gutterBottom sx={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; color: 'primary.main', fontWeight: 'bold', mt: 3 }}>
                ⭐ 5. Critérios de Avaliação
              </Typography>
              <Divider sx={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; mb: 2 }} />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12}>
              <TextField
                fullWidth
                multiline
                rows={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;3}
                label="Resolutividade"
                value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.resolutividade}
                onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('resolutividade')}
                inputProps={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; maxLength: 500 }}
                helperText={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;helpers.getMensagemLimite('resolutividade')}
              />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12} md={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;6}>
              <TextField
                fullWidth
                multiline
                rows={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;3}
                label="Inovação"
                value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.inovacao}
                onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('inovacao')}
                inputProps={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; maxLength: 500 }}
                helperText={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;helpers.getMensagemLimite('inovacao')}
              />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12} md={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;6}>
              <TextField
                fullWidth
                multiline
                rows={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;3}
                label="Transparência"
                value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.transparencia}
                onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('transparencia')}
                inputProps={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; maxLength: 500 }}
                helperText={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;helpers.getMensagemLimite('transparencia')}
              />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12} md={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;6}>
              <TextField
                fullWidth
                multiline
                rows={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;3}
                label="Proatividade"
                value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.proatividade}
                onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('proatividade')}
                inputProps={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; maxLength: 500 }}
                helperText={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;helpers.getMensagemLimite('proatividade')}
              />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12} md={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;6}>
              <TextField
                fullWidth
                multiline
                rows={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;3}
                label="Cooperação"
                value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.cooperacao}
                onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('cooperacao')}
                inputProps={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; maxLength: 500 }}
                helperText={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;helpers.getMensagemLimite('cooperacao')}
              />
            </Grid>

            {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;/* SEÇÃO 6: RESULTADOS */}
            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12}>
              <Typography variant="h6" gutterBottom sx={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; color: 'primary.main', fontWeight: 'bold', mt: 3 }}>
                📊 6. Resultados Alcançados
              </Typography>
              <Divider sx={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; mb: 2 }} />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12} md={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;4}>
              <TextField
                fullWidth
                label="Resultado 1"
                value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.resultado_1}
                onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('resultado_1')}
                inputProps={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; maxLength: 100 }}
                helperText={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;helpers.getMensagemLimite('resultado_1')}
              />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12} md={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;4}>
              <TextField
                fullWidth
                label="Resultado 2"
                value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.resultado_2}
                onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('resultado_2')}
                inputProps={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; maxLength: 100 }}
                helperText={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;helpers.getMensagemLimite('resultado_2')}
              />
            </Grid>

            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12} md={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;4}>
              <TextField
                fullWidth
                label="Resultado 3"
                value={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;formData.resultado_3}
                onChange={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;handleChange('resultado_3')}
                inputProps={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; maxLength: 100 }}
                helperText={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;helpers.getMensagemLimite('resultado_3')}
              />
            </Grid>

            {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;/* BOTÕES DE AÇÃO */}
            <Grid item xs={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;12}>
              <Box sx={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;{
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null; display: 'flex', gap: 2, justifyContent: 'flex-end', mt: 4 }}>
                <Button
                  variant="outlined"
                  startIcon={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;<ArrowBack />}
                  onClick={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;() => navigate('/projects')}
                  disabled={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;saving}
                >
                  Cancelar
                </Button>
                <Button
                  type="submit"
                  variant="contained"
                  startIcon={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;<Save />}
                  disabled={
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;saving}
                  size="large"
                >
                  {
  const location = useLocation();
  const prefill = (location && location.state && location.state.prefill) || null;saving ? 'Salvando...' : (isEdit ? 'Atualizar Projeto' : 'Criar Projeto')}
                </Button>
              </Box>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Container>
  );
};

export default ProjectForm;
// Prefill from chat
// eslint-disable-next-line
try { if (prefill && typeof setForm==='function') { setForm((prev)=>({ ...prev, ...prefill })); } } catch(e) {}
