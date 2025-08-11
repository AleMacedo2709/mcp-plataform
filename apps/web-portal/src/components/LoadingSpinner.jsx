import React from 'react'
import { CircularProgress, Box } from '@mui/material'

export default function LoadingSpinner() {
  return (
    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', p: 4 }}>
      <CircularProgress />
    </Box>
  )
}
