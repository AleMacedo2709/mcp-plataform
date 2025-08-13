import { useEffect, useMemo, useState } from 'react'
import { useMsal } from '@azure/msal-react'

export function useAuth() {
  const { accounts, instance } = useMsal()
  const [token, setToken] = useState('')
  const isTest = process.env.REACT_APP_TEST_MODE === 'true'

  const user = useMemo(() => {
    if (isTest) {
      // Em DEV, token vazio (WS aceitará sem auth)
      return { name: 'Usuário de Teste', email: 'teste@mp.local', token }
    }
    const acc = accounts?.[0]
    // Ajuste aqui para extrair token/claims do MSAL se necessário
    return acc ? { name: acc.name, email: acc.username, token } : null
  }, [accounts, isTest, token])

  useEffect(() => {
    if (isTest) { setToken(''); return }
    const acc = accounts?.[0]
    if (!acc) { setToken(''); return }
    // Tenta obter access token (ajuste os scopes conforme seu AAD/API)
    instance.acquireTokenSilent({ scopes: ['User.Read'], account: acc })
      .then(r => setToken(r?.accessToken || ''))
      .catch(() => setToken(''))
  }, [accounts, instance, isTest])

  const hasPermission = (role) => {
    // Modo teste: permitir tudo
    if (isTest) return true
    // Produção: ajuste conforme claims/roles do Azure AD quando necessário
    return !!user
  }

  return { isLoading: false, user, hasPermission }
}
