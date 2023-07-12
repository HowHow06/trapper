import PropTypes from 'prop-types'
import { useEffect, useRef, useState } from 'react'
import api from '../api'
import { isApiSuccess } from '../utils/api-call'

export const AuthGuard = (props) => {
  const { children } = props
  const ignore = useRef(false)
  const [checked, setChecked] = useState(false)

  useEffect(() => {
    const initialize = async () => {
      // Prevent from calling twice in development mode with React.StrictMode enabled
      if (ignore.current) {
        return
      }

      ignore.current = true

      let isAuthenticated = false

      const response = await api.testToken()
      if (isApiSuccess(response)) {
        console.log('Legit User!', response.data)
        isAuthenticated = true
      } else {
        console.log('Test Token failed', response.error)
      }

      if (!isAuthenticated) {
        // open the login page of the UI console panel
        const loginLink = `${import.meta.env.VITE_CONSOLE_PANEL_URL}${
          import.meta.env.VITE_CONSOLE_PANEL_LOGIN_PATH
        }`
        const continueUrl = encodeURIComponent(window.location.href)
        window.location.href = `${loginLink}?continueUrl=${continueUrl}`
      } else {
        setChecked(true)
      }
    }

    initialize()
  }, [])

  if (!checked) {
    return null
  }

  return children
}

AuthGuard.propTypes = {
  children: PropTypes.node,
}
