import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

// MSAL (mantemos provider, mesmo em teste)
import { PublicClientApplication, EventType } from '@azure/msal-browser'
import { MsalProvider } from '@azure/msal-react'

import App from './App'

const isTest = process.env.REACT_APP_TEST_MODE === 'true'

const msalInstance = new PublicClientApplication({
  auth: {
    clientId: process.env.REACT_APP_AAD_CLIENT_ID || '00000000-0000-0000-0000-000000000000',
    authority: process.env.REACT_APP_AAD_TENANT_ID
      ? `https://login.microsoftonline.com/${process.env.REACT_APP_AAD_TENANT_ID}`
      : 'https://login.microsoftonline.com/common',
    redirectUri: window.location.origin
  },
  cache: {
    cacheLocation: 'sessionStorage',
    storeAuthStateInCookie: false,
  }
})

// Em modo teste, não faremos login, mas mantemos provider para compatibilidade
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <MsalProvider instance={msalInstance}>
      <BrowserRouter>
        <App />
        <ToastContainer position="top-right" autoClose={3000} />
      </BrowserRouter>
    </MsalProvider>
  </React.StrictMode>
)
