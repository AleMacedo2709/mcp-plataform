import { createTheme } from '@mui/material'
import { colors, typography, shape } from './tokens'

export const appTheme = createTheme({
  typography: { fontFamily: typography.fontFamily },
  palette: {
    mode: 'light',
    primary: { main: colors.brand.primary },
    secondary: { main: colors.brand.secondary },
    success: { main: colors.state.success },
    warning: { main: colors.state.warning },
    error: { main: colors.state.danger },
    info: { main: colors.state.info },
    background: { default: colors.neutral[50], paper: colors.neutral[100] },
    text: { primary: colors.neutral[900], secondary: colors.neutral[400] },
    divider: colors.borders.subtle
  },
  shape: { borderRadius: shape.radius },
  components: {
    MuiButton: {
      defaultProps: { size: 'medium' },
      styleOverrides: {
        root: { textTransform: 'none', fontWeight: 700, borderRadius: shape.radius - 4 },
        containedPrimary: {
          background: `linear-gradient(135deg, ${colors.brand.red} 0%, ${colors.brand.redMuted} 100%)`,
          boxShadow: '0 10px 24px rgba(211,47,47,0.25)',
          '&:hover': {
            background: `linear-gradient(135deg, ${colors.brand.redMuted} 0%, ${colors.brand.red} 100%)`,
            boxShadow: '0 12px 28px rgba(211,47,47,0.35)'
          }
        }
      }
    },
    MuiCard: {
      styleOverrides: { root: { backgroundImage: 'none', backgroundColor: colors.neutral[100], border: `1px solid ${colors.borders.subtle}`, boxShadow: 'var(--shadow-sm, 0 1px 2px rgba(17,24,39,0.06))' } }
    },
    MuiPaper: { styleOverrides: { root: { backgroundImage: 'none' } } },
    MuiOutlinedInput: {
      styleOverrides: {
        root: { backgroundColor: 'rgba(255,255,255,0.04)' },
        notchedOutline: { borderColor: colors.borders.subtle }
      }
    },
    MuiTextField: { defaultProps: { size: 'small', variant: 'outlined' } },
    MuiSelect: { defaultProps: { size: 'small' } },
    MuiInputLabel: { styleOverrides: { root: { color: colors.neutral[300] } } },
    MuiChip: { styleOverrides: { root: { borderRadius: shape.radius - 6 } } },
    MuiCardContent: { styleOverrides: { root: { padding: 16 } } },
    MuiAppBar: { styleOverrides: { root: { backgroundColor: colors.neutral[100], backgroundImage: 'none', borderBottom: `1px solid ${colors.borders.subtle}` } } },
    MuiDataGrid: {
      styleOverrides: {
        root: { backgroundColor: 'transparent', border: `1px solid ${colors.borders.subtle}` },
        columnHeaders: { background: '#f9fafb', borderBottom: `1px solid ${colors.borders.subtle}`, color: colors.neutral[900] },
        cell: { borderBottom: `1px solid ${colors.borders.subtle}` },
        footerContainer: { borderTop: `1px solid ${colors.borders.subtle}` }
      }
    }
  }
})


