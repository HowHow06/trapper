import React from 'react'
import ReactDOM from 'react-dom/client'
import { AuthGuard } from '../guards/auth-guard'
import '../theme.scss'
import App from './Options'

ReactDOM.createRoot(document.getElementById('app')).render(
  <React.StrictMode>
    <AuthGuard>
      <App />
    </AuthGuard>
  </React.StrictMode>,
)
