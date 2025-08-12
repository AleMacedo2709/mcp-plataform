import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')

  // Mapear REACT_APP_* para compatibilidade com os arquivos enviados
  const reactEnv = {
    REACT_APP_TEST_MODE: env.VITE_TEST_MODE ?? process.env.REACT_APP_TEST_MODE ?? 'true',
    REACT_APP_API_BASE_URL: env.VITE_API_BASE_URL ?? process.env.REACT_APP_API_BASE_URL ?? 'http://localhost:18000',
    REACT_APP_INGESTION_BASE_URL: env.VITE_INGESTION_BASE_URL ?? process.env.REACT_APP_INGESTION_BASE_URL ?? 'http://localhost:18001',
    REACT_APP_AAD_CLIENT_ID: env.VITE_AAD_CLIENT_ID ?? process.env.REACT_APP_AAD_CLIENT_ID ?? '',
    REACT_APP_AAD_TENANT_ID: env.VITE_AAD_TENANT_ID ?? process.env.REACT_APP_AAD_TENANT_ID ?? '',
    REACT_APP_CHAT_BASE_URL: env.VITE_CHAT_BASE_URL ?? process.env.REACT_APP_CHAT_BASE_URL ?? 'http://localhost:18002'
  }

  return {
    plugins: [react()],
    define: {
      'process.env': { ...reactEnv }
    },
    server: {
      port: 5173,
      host: true
    }
  }
})
