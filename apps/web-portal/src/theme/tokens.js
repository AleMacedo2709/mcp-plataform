// Design tokens centralizados (cores, tipografia, espaçamentos) – Light mode institucional

export const colors = {
  brand: {
    primary: '#b30021',
    primary600: '#93001b',
    secondary: '#0b4d79',
    secondary600: '#093e61',
  },
  neutral: {
    50: '#f7f7f9',
    100: '#ffffff',
    200: '#e5e7eb',
    400: '#6b7280',
    900: '#111827',
  },
  state: {
    success: '#0f766e',
    warning: '#b45309',
    danger: '#b91c1c',
    info: '#1d4ed8',
  },
  borders: {
    subtle: '#e5e7eb',
    strong: '#d1d5db'
  }
}

export const typography = {
  fontFamily:
    "system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', 'Apple Color Emoji', 'Segoe UI Emoji'",
}

export const shape = {
  radius: 12,
}

export const spacing = (n) => n * 4


