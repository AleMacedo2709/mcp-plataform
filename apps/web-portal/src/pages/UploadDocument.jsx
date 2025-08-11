import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  Alert,
  Card,
  CardContent,
  Grid
} from '@mui/material';
import { AutoAwesome, ArrowBack, SmartToy } from '@mui/icons-material';

const UploadDocument = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1">
          📤 Upload de Documentos
        </Typography>
        <Button
          variant="outlined"
          startIcon={<ArrowBack />}
          onClick={() => navigate('/dashboard')}
        >
          Voltar
        </Button>
      </Box>

      <Alert severity="success" sx={{ mb: 3 }}>
        <strong>🤖 Funcionalidade Inteligente Disponível!</strong><br/>
        A funcionalidade de upload + análise IA + preenchimento automático está implementada na <strong>Criação Inteligente de Projeto</strong>.
      </Alert>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%', cursor: 'pointer' }} onClick={() => navigate('/projects/smart-create')}>
            <CardContent sx={{ textAlign: 'center', p: 4 }}>
              <SmartToy sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
              <Typography variant="h5" gutterBottom color="primary">
                🤖 Criação Inteligente
              </Typography>
              <Typography variant="body1" paragraph>
                <strong>Upload + IA + Formulário Completo</strong>
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                • Envie PDF, DOCX ou TXT<br/>
                • IA extrai TODOS os 29 campos do Prêmio CNMP<br/>
                • Formulário pré-preenchido para edição<br/>
                • Salva projeto automaticamente
              </Typography>
              <Button 
                variant="contained" 
                startIcon={<AutoAwesome />}
                onClick={() => navigate('/projects/smart-create')}
                sx={{ mt: 2 }}
              >
                Usar Criação Inteligente
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ textAlign: 'center', p: 4 }}>
              <Typography variant="h5" gutterBottom>
                📝 Upload Simples
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Funcionalidade básica de upload de documentos<br/>
                <em>(Será implementada pela TI conforme necessário)</em>
              </Typography>
              <Alert severity="info" sx={{ mt: 2 }}>
                Para análise inteligente com IA, use a <strong>Criação Inteligente</strong> ao lado.
              </Alert>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          🎯 Como Funciona a Criação Inteligente:
        </Typography>
        
        <Box sx={{ ml: 2 }}>
          <Typography variant="body2" paragraph>
            <strong>1. Upload:</strong> Envie um documento (PDF, DOCX, TXT) com informações do projeto
          </Typography>
          <Typography variant="body2" paragraph>
            <strong>2. Análise IA:</strong> Sistema extrai automaticamente dados para os 29 campos do formulário Prêmio CNMP 2025
          </Typography>
          <Typography variant="body2" paragraph>
            <strong>3. Edição:</strong> Revise e edite os dados extraídos no formulário completo
          </Typography>
          <Typography variant="body2" paragraph>
            <strong>4. Salvamento:</strong> Projeto salvo automaticamente na base de dados
          </Typography>
        </Box>

        <Box sx={{ mt: 3, textAlign: 'center' }}>
          <Button 
            variant="contained" 
            size="large"
            startIcon={<SmartToy />}
            onClick={() => navigate('/projects/smart-create')}
          >
            Experimentar Agora
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default UploadDocument;