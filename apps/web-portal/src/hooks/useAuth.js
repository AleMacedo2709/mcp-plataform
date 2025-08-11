import { useMemo } from 'react'
import { useMsal } from '@azure/msal-react'

export function useAuth() {
  const { accounts } = useMsal()
  const isTest = process.env.REACT_APP_TEST_MODE === 'true'

  const user = useMemo(() => {
    if (isTest) {
      return { name: 'Usuário de Teste', email: 'teste@mp.local' }
    }
    const acc = accounts?.[0]
    return acc ? { name: acc.name, email: acc.username } : null
  }, [accounts, isTest])

  return { isLoading: false, user }
}
