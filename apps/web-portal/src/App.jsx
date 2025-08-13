import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useIsAuthenticated } from '@azure/msal-react';
import { Box } from '@mui/material';

// Components
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import ProjectList from './pages/ProjectList';
import ProjectForm from './pages/ProjectForm';
import ProjectView from './pages/ProjectView';
// import UploadDocument from './pages/UploadDocument';
import SmartProjectCreator from './pages/SmartProjectCreator'
import Chat from './pages/Chat'
// Removed Processamentos pages
// import Profile from './pages/Profile';
import LoadingSpinner from './components/LoadingSpinner';
import MyProjects from './pages/MyProjects';

// Hooks
import { useAuth } from './hooks/useAuth';

function App() {
  // 🔧 CONFIGURAÇÃO: Modo teste ou produção
  // Para TESTE (sem autenticação): REACT_APP_TEST_MODE=true
  // Para PRODUÇÃO (com Azure AD): REACT_APP_TEST_MODE=false ou remover
  const isTestMode = process.env.REACT_APP_TEST_MODE === 'true';
  
  // Autenticação do Azure AD (apenas em produção)
  const isAuthenticated = useIsAuthenticated();
  const { isLoading, user } = useAuth();

  // Usuário fictício para modo de teste
  const testUser = {
    name: "Usuário Teste",
    email: "teste@mpsp.mp.br",
    department: "CGE - Gestão de Inovação",
    roles: ["admin"]
  };

  // 🔐 MODO PRODUÇÃO: Verificar autenticação Azure AD
  if (!isTestMode) {
    if (isLoading) {
      return <LoadingSpinner />;
    }

    if (!isAuthenticated) {
      return <Login />;
    }
  }

  // 🎯 ROTAS PRINCIPAIS (compartilhadas entre teste e produção)
  const currentUser = isTestMode ? testUser : user;

  return (
    <Box sx={{ width: '100%', flex: '1 1 auto' }}>
      <Layout user={currentUser}>
        <Routes>
          {/* Dashboard Principal */}
          <Route path="/" element={<Dashboard />} />
          <Route path="/dashboard" element={<Dashboard />} />
          
          {/* Gestão de Projetos */}
          <Route path="/projects" element={<ProjectList />} />
          <Route path="/projects/new" element={<ProjectForm />} />
          <Route path="/projects/smart-create" element={<SmartProjectCreator />} />
          <Route path="/projects/:id" element={<ProjectView />} />
          <Route path="/projects/:id/edit" element={<ProjectForm />} />
          <Route path="/my-projects" element={<MyProjects />} />
          
          {/* Upload e Perfil removidos temporariamente */}
          {/* <Route path="/upload" element={<UploadDocument />} /> */}
          {/* <Route path="/profile" element={<Profile />} /> */}
          
          {/* Redirecionamento padrão */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />

          <Route path="/chat" element={<Chat />} />
      </Routes>
      </Layout>
    </Box>
  );
}

export default App;