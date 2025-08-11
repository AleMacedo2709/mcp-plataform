import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  Alert,
  LinearProgress,
  Stepper,
  Step,
  StepLabel,
  Grid,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Divider
} from '@mui/material';
import {
  CloudUpload,
  AutoAwesome,
  Edit,
  Save,
  ArrowBack
} from '@mui/icons-material';
import { toast } from 'react-toastify';

import { uploadDocument, createProject } from '../services/apiService';
import {
  TIPOS_INICIATIVA,
  CLASSIFICACOES,
  FASES_IMPLEMENTACAO,
  CATEGORIAS,
  OBJETIVOS_ESTRATEGICOS,
  helpers
} from '../constants/formOptions';

const SmartProjectCreator = () => {
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(0);
  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [file, setFile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [projectData, setProjectData] = useState({
    // Campos obrigatórios Prêmio CNMP 2025
    nome_iniciativa: '',
    tipo_iniciativa: '',
    classificacao: '',
    natureza_iniciativa: '',
    iniciativa_vinculada: '',
    objetivo_estrategico_pen_mp: '',
    programa_pen_mp: [],
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
    comprovacao_resultados: null,
    capa_iniciativa: null,
    categoria: ''
  });

  const steps = [
    'Upload do Documento',
    'Análise por IA',
    'Edição dos Dados',
    'Confirmação'
  ];

  // Opções do formulário importadas das constantes compartilhadas
  // (Removidas duplicações - agora usa formOptions.js)

  const handleFileUpload = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      // Validar tipo de arquivo
      const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
      if (!allowedTypes.includes(selectedFile.type)) {
        toast.error('Tipo de arquivo não suportado. Use PDF, DOCX ou TXT.');
        return;
      }

      // Validar tamanho (50MB max)
      if (selectedFile.size > 50 * 1024 * 1024) {
        toast.error('Arquivo muito grande. Máximo 50MB.');
        return;
      }

      setFile(selectedFile);
      setActiveStep(1);
      analyzeDocument(selectedFile);
    }
  };

  const analyzeDocument = async (file) => {
    setAnalyzing(true);
    try {
      toast.info('🤖 Analisando documento com IA...');
      
      const result = await uploadDocument(file, 'analyze_project_document_cnmp');
      
      if (result && result.analysis) {
        setAnalysisResult(result);
        
        // Pré-preencher formulário com dados da IA - TODOS OS 29 CAMPOS
        const analysis = result.analysis;
        setProjectData({
          nome_iniciativa: analysis.nome_iniciativa || analysis.titulo || '',
          tipo_iniciativa: analysis.tipo_iniciativa || '',
          classificacao: analysis.classificacao || '',
          natureza_iniciativa: analysis.natureza_iniciativa || analysis.natureza || '',
          iniciativa_vinculada: analysis.iniciativa_vinculada || '',
          objetivo_estrategico_pen_mp: analysis.objetivo_estrategico_pen_mp || '',
          programa_pen_mp: analysis.programa_pen_mp || [],
          promocao_objetivo_estrategico: analysis.promocao_objetivo_estrategico || '',
          data_inicial_operacao: analysis.data_inicial_operacao || analysis.data_inicio || '',
          fase_implementacao: analysis.fase_implementacao || analysis.fase || '',
          descricao: analysis.descricao || analysis.resumo || '',
          estimativa_recursos: analysis.estimativa_recursos || analysis.recursos || '',
          publico_impactado: analysis.publico_impactado || analysis.publico || '',
          orgaos_envolvidos: analysis.orgaos_envolvidos || analysis.parceiros || '',
          contatos: analysis.contatos || analysis.responsavel || '',
          desafio_1: analysis.desafio_1 || analysis.desafios?.[0] || '',
          desafio_2: analysis.desafio_2 || analysis.desafios?.[1] || '',
          desafio_3: analysis.desafio_3 || analysis.desafios?.[2] || '',
          resolutividade: analysis.resolutividade || '',
          inovacao: analysis.inovacao || '',
          transparencia: analysis.transparencia || '',
          proatividade: analysis.proatividade || '',
          cooperacao: analysis.cooperacao || '',
          resultado_1: analysis.resultado_1 || analysis.resultados?.[0] || '',
          resultado_2: analysis.resultado_2 || analysis.resultados?.[1] || '',
          resultado_3: analysis.resultado_3 || analysis.resultados?.[2] || '',
          comprovacao_resultados: null,
          capa_iniciativa: null,
          categoria: analysis.categoria || ''
        });
        
        setActiveStep(2);
        toast.success('✅ Documento analisado! Dados extraídos automaticamente.');
      } else {
        throw new Error('Análise não retornou dados válidos');
      }
    } catch (error) {
      console.error('Erro na análise:', error);
      toast.error('❌ Erro ao analisar documento. Tente novamente.');
      setActiveStep(0);
      setFile(null);
    } finally {
      setAnalyzing(false);
    }
  };

  const handleInputChange = (field, value) => {
    setProjectData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSaveProject = async () => {
    setSaving(true);
    try {
      // Validação básica
      if (!projectData.nome_iniciativa.trim()) {
        toast.error('Nome da iniciativa é obrigatório');
        return;
      }

      const result = await createProject(projectData);
      
      if (result) {
        setActiveStep(3);
        toast.success('🎉 Projeto criado com sucesso!');
        
        // Redirecionar após 2 segundos
        setTimeout(() => {
          navigate('/projects');
        }, 2000);
      }
    } catch (error) {
      console.error('Erro ao salvar:', error);
      toast.error('❌ Erro ao salvar projeto. Tente novamente.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1">
          🤖 Criação Inteligente de Projeto
        </Typography>
        <Button
          variant="outlined"
          startIcon={<ArrowBack />}
          onClick={() => navigate('/projects')}
        >
          Voltar
        </Button>
      </Box>

      {/* Stepper */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Stepper activeStep={activeStep} alternativeLabel>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
      </Paper>

      {/* Step 0: Upload */}
      {activeStep === 0 && (
        <Paper sx={{ p: 4 }}>
          <Box sx={{ textAlign: 'center' }}>
            <CloudUpload sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
            <Typography variant="h5" gutterBottom>
              Upload do Documento
            </Typography>
            <Typography variant="body1" color="text.secondary" paragraph>
              Envie um documento (PDF, DOCX ou TXT) e nossa IA extrairá automaticamente os dados do projeto.
            </Typography>
            
            <input
              accept=".pdf,.docx,.txt"
              style={{ display: 'none' }}
              id="upload-file"
              type="file"
              onChange={handleFileUpload}
            />
            <label htmlFor="upload-file">
              <Button
                variant="contained"
                component="span"
                size="large"
                startIcon={<CloudUpload />}
                sx={{ mt: 2 }}
              >
                Selecionar Documento
              </Button>
            </label>

            <Typography variant="caption" display="block" sx={{ mt: 2 }}>
              Formatos aceitos: PDF, DOCX, TXT • Tamanho máximo: 50MB
            </Typography>
          </Box>
        </Paper>
      )}

      {/* Step 1: Analyzing */}
      {activeStep === 1 && (
        <Paper sx={{ p: 4 }}>
          <Box sx={{ textAlign: 'center' }}>
            <AutoAwesome sx={{ fontSize: 64, color: 'secondary.main', mb: 2 }} />
            <Typography variant="h5" gutterBottom>
              Analisando com IA...
            </Typography>
            <Typography variant="body1" color="text.secondary" paragraph>
              Arquivo: <strong>{file?.name}</strong>
            </Typography>
            <LinearProgress sx={{ mb: 2 }} />
            <Typography variant="body2" color="text.secondary">
              Processando documento e extraindo informações do projeto...
            </Typography>
          </Box>
        </Paper>
      )}

      {/* Step 2: Edit Form */}
      {activeStep === 2 && (
        <Paper sx={{ p: 4 }}>
          <Box sx={{ mb: 3, display: 'flex', alignItems: 'center' }}>
            <Edit sx={{ mr: 1 }} />
            <Typography variant="h5">
              Editar Dados do Projeto
            </Typography>
          </Box>

          {analysisResult && (
            <Alert severity="success" sx={{ mb: 3 }}>
              ✅ Dados extraídos automaticamente do documento. Revise e edite conforme necessário.
            </Alert>
          )}

          <Grid container spacing={3}>
            {/* SEÇÃO 1: IDENTIFICAÇÃO DA INICIATIVA */}
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom sx={{ color: 'primary.main', fontWeight: 'bold' }}>
                📋 1. Identificação da Iniciativa
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Nome da Iniciativa *"
                value={projectData.nome_iniciativa}
                onChange={(e) => handleInputChange('nome_iniciativa', e.target.value)}
                required
                inputProps={{ maxLength: 300 }}
                helperText="Título da iniciativa inscrita no Prêmio (máx. 300 caracteres)"
              />
            </Grid>

            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>Tipo de Iniciativa *</InputLabel>
                <Select
                  value={projectData.tipo_iniciativa}
                  onChange={(e) => handleInputChange('tipo_iniciativa', e.target.value)}
                  required
                >
                  {TIPOS_INICIATIVA.map(tipo => (
                    <MenuItem key={tipo} value={tipo}>{helpers.getIconeTipo(tipo)} {tipo}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>Classificação *</InputLabel>
                <Select
                  value={projectData.classificacao}
                  onChange={(e) => handleInputChange('classificacao', e.target.value)}
                  required
                >
                  {CLASSIFICACOES.map(classe => (
                    <MenuItem key={classe} value={classe}>{classe}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>Categoria *</InputLabel>
                <Select
                  value={projectData.categoria}
                  onChange={(e) => handleInputChange('categoria', e.target.value)}
                  required
                >
                  {CATEGORIAS.map(cat => (
                    <MenuItem key={cat} value={cat}>{cat}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Natureza da Iniciativa"
                value={projectData.natureza_iniciativa}
                onChange={(e) => handleInputChange('natureza_iniciativa', e.target.value)}
                inputProps={{ maxLength: 100 }}
                helperText="Resumo da natureza da iniciativa (máx. 100 caracteres)"
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Iniciativa Vinculada"
                value={projectData.iniciativa_vinculada}
                onChange={(e) => handleInputChange('iniciativa_vinculada', e.target.value)}
                inputProps={{ maxLength: 300 }}
                helperText="Nome da iniciativa e instituição vinculada (máx. 300 caracteres)"
              />
            </Grid>

            {/* SEÇÃO 2: ALINHAMENTO ESTRATÉGICO */}
            <Grid item xs={12}>
              <Divider sx={{ my: 2 }} />
              <Typography variant="h6" gutterBottom sx={{ color: 'primary.main', fontWeight: 'bold' }}>
                🎯 2. Alinhamento Estratégico PEN-MP
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Objetivo Estratégico PEN-MP</InputLabel>
                <Select
                  value={projectData.objetivo_estrategico_pen_mp}
                  onChange={(e) => handleInputChange('objetivo_estrategico_pen_mp', e.target.value)}
                >
                  {OBJETIVOS_ESTRATEGICOS.map(obj => (
                    <MenuItem key={obj} value={obj}>{obj}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                multiline
                rows={2}
                label="Promoção do Objetivo Estratégico"
                value={projectData.promocao_objetivo_estrategico}
                onChange={(e) => handleInputChange('promocao_objetivo_estrategico', e.target.value)}
                inputProps={{ maxLength: 100 }}
                helperText="Como a iniciativa contribui para o objetivo estratégico (máx. 100 caracteres)"
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Data Inicial de Operação"
                value={projectData.data_inicial_operacao}
                onChange={(e) => handleInputChange('data_inicial_operacao', e.target.value)}
                type="date"
                InputLabelProps={{ shrink: true }}
                helperText="Data em que a iniciativa começou a operar"
              />
            </Grid>

            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Fase de Implementação</InputLabel>
                <Select
                  value={projectData.fase_implementacao}
                  onChange={(e) => handleInputChange('fase_implementacao', e.target.value)}
                >
                  {FASES_IMPLEMENTACAO.map(fase => (
                    <MenuItem key={fase} value={fase}>{fase}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            {/* SEÇÃO 3: DESCRIÇÃO DETALHADA */}
            <Grid item xs={12}>
              <Divider sx={{ my: 2 }} />
              <Typography variant="h6" gutterBottom sx={{ color: 'primary.main', fontWeight: 'bold' }}>
                📝 3. Descrição da Iniciativa
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={5}
                label="Descrição Detalhada *"
                value={projectData.descricao}
                onChange={(e) => handleInputChange('descricao', e.target.value)}
                required
                inputProps={{ maxLength: 1000 }}
                helperText="Descrição detalhada da iniciativa (máx. 1000 caracteres)"
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                multiline
                rows={2}
                label="Estimativa de Recursos"
                value={projectData.estimativa_recursos}
                onChange={(e) => handleInputChange('estimativa_recursos', e.target.value)}
                inputProps={{ maxLength: 200 }}
                helperText="Recursos materiais e humanos necessários (máx. 200 caracteres)"
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Público Impactado"
                value={projectData.publico_impactado}
                onChange={(e) => handleInputChange('publico_impactado', e.target.value)}
                inputProps={{ maxLength: 100 }}
                helperText="Público interno/externo impactado (máx. 100 caracteres)"
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                multiline
                rows={2}
                label="Órgãos Envolvidos"
                value={projectData.orgaos_envolvidos}
                onChange={(e) => handleInputChange('orgaos_envolvidos', e.target.value)}
                inputProps={{ maxLength: 300 }}
                helperText="Órgãos parceiros ou colaboradores (máx. 300 caracteres)"
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                multiline
                rows={2}
                label="Contatos"
                value={projectData.contatos}
                onChange={(e) => handleInputChange('contatos', e.target.value)}
                inputProps={{ maxLength: 300 }}
                helperText="Nome e e-mail dos responsáveis (máx. 300 caracteres)"
              />
            </Grid>

            {/* SEÇÃO 4: DESAFIOS */}
            <Grid item xs={12}>
              <Divider sx={{ my: 2 }} />
              <Typography variant="h6" gutterBottom sx={{ color: 'primary.main', fontWeight: 'bold' }}>
                ⚡ 4. Desafios Enfrentados
              </Typography>
            </Grid>

            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Desafio 1"
                value={projectData.desafio_1}
                onChange={(e) => handleInputChange('desafio_1', e.target.value)}
                inputProps={{ maxLength: 100 }}
                helperText="Primeiro desafio (máx. 100 caracteres)"
              />
            </Grid>

            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Desafio 2"
                value={projectData.desafio_2}
                onChange={(e) => handleInputChange('desafio_2', e.target.value)}
                inputProps={{ maxLength: 100 }}
                helperText="Segundo desafio (máx. 100 caracteres)"
              />
            </Grid>

            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Desafio 3"
                value={projectData.desafio_3}
                onChange={(e) => handleInputChange('desafio_3', e.target.value)}
                inputProps={{ maxLength: 100 }}
                helperText="Terceiro desafio (máx. 100 caracteres)"
              />
            </Grid>

            {/* SEÇÃO 5: CRITÉRIOS DE AVALIAÇÃO */}
            <Grid item xs={12}>
              <Divider sx={{ my: 2 }} />
              <Typography variant="h6" gutterBottom sx={{ color: 'primary.main', fontWeight: 'bold' }}>
                ⭐ 5. Critérios de Avaliação
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={3}
                label="Resolutividade"
                value={projectData.resolutividade}
                onChange={(e) => handleInputChange('resolutividade', e.target.value)}
                inputProps={{ maxLength: 500 }}
                helperText="Justificativa quanto à resolutividade (máx. 500 caracteres)"
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                multiline
                rows={3}
                label="Inovação"
                value={projectData.inovacao}
                onChange={(e) => handleInputChange('inovacao', e.target.value)}
                inputProps={{ maxLength: 500 }}
                helperText="Justificativa quanto à inovação (máx. 500 caracteres)"
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                multiline
                rows={3}
                label="Transparência"
                value={projectData.transparencia}
                onChange={(e) => handleInputChange('transparencia', e.target.value)}
                inputProps={{ maxLength: 500 }}
                helperText="Justificativa quanto à transparência (máx. 500 caracteres)"
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                multiline
                rows={3}
                label="Proatividade"
                value={projectData.proatividade}
                onChange={(e) => handleInputChange('proatividade', e.target.value)}
                inputProps={{ maxLength: 500 }}
                helperText="Justificativa quanto à proatividade (máx. 500 caracteres)"
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                multiline
                rows={3}
                label="Cooperação"
                value={projectData.cooperacao}
                onChange={(e) => handleInputChange('cooperacao', e.target.value)}
                inputProps={{ maxLength: 500 }}
                helperText="Justificativa quanto à cooperação (máx. 500 caracteres)"
              />
            </Grid>

            {/* SEÇÃO 6: RESULTADOS */}
            <Grid item xs={12}>
              <Divider sx={{ my: 2 }} />
              <Typography variant="h6" gutterBottom sx={{ color: 'primary.main', fontWeight: 'bold' }}>
                📊 6. Resultados Alcançados
              </Typography>
            </Grid>

            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Resultado 1"
                value={projectData.resultado_1}
                onChange={(e) => handleInputChange('resultado_1', e.target.value)}
                inputProps={{ maxLength: 100 }}
                helperText="Primeiro resultado (máx. 100 caracteres)"
              />
            </Grid>

            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Resultado 2"
                value={projectData.resultado_2}
                onChange={(e) => handleInputChange('resultado_2', e.target.value)}
                inputProps={{ maxLength: 100 }}
                helperText="Segundo resultado (máx. 100 caracteres)"
              />
            </Grid>

            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Resultado 3"
                value={projectData.resultado_3}
                onChange={(e) => handleInputChange('resultado_3', e.target.value)}
                inputProps={{ maxLength: 100 }}
                helperText="Terceiro resultado (máx. 100 caracteres)"
              />
            </Grid>

            {/* SEÇÃO 7: ANEXOS (Preparado para futura implementação) */}
            <Grid item xs={12}>
              <Divider sx={{ my: 2 }} />
              <Typography variant="h6" gutterBottom sx={{ color: 'primary.main', fontWeight: 'bold' }}>
                📎 7. Anexos (Será implementado pela TI)
              </Typography>
            </Grid>

            <Grid item xs={12} md={6}>
              <Alert severity="info">
                📄 <strong>Comprovação dos Resultados:</strong><br/>
                Upload de arquivos que comprovam os resultados<br/>
                <em>(Funcionalidade será implementada pela TI)</em>
              </Alert>
            </Grid>

            <Grid item xs={12} md={6}>
              <Alert severity="info">
                🖼️ <strong>Capa da Iniciativa:</strong><br/>
                Imagem da iniciativa (JPG/PNG)<br/>
                <em>(Funcionalidade será implementada pela TI)</em>
              </Alert>
            </Grid>
          </Grid>

          <Box sx={{ mt: 4, display: 'flex', justifyContent: 'space-between' }}>
            <Button
              variant="outlined"
              onClick={() => {
                setActiveStep(0);
                setFile(null);
                setAnalysisResult(null);
              }}
            >
              Voltar ao Upload
            </Button>
            
            <Button
              variant="contained"
              size="large"
              startIcon={<Save />}
              onClick={handleSaveProject}
              disabled={saving || !projectData.nome_iniciativa.trim()}
            >
              {saving ? 'Salvando...' : 'Salvar Projeto'}
            </Button>
          </Box>
        </Paper>
      )}

      {/* Step 3: Success */}
      {activeStep === 3 && (
        <Paper sx={{ p: 4 }}>
          <Box sx={{ textAlign: 'center' }}>
            <Save sx={{ fontSize: 64, color: 'success.main', mb: 2 }} />
            <Typography variant="h5" gutterBottom color="success.main">
              🎉 Projeto Criado com Sucesso!
            </Typography>
            <Typography variant="body1" color="text.secondary" paragraph>
              O projeto "{projectData.nome_iniciativa}" foi salvo na base de dados.
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Redirecionando para a lista de projetos...
            </Typography>
          </Box>
        </Paper>
      )}
    </Container>
  );
};

export default SmartProjectCreator;