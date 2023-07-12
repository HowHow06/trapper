import React from 'react'
import { Button, Stack } from 'react-bootstrap'

const LoginPrompt = () => {
  const loginLink = `${import.meta.env.VITE_CONSOLE_PANEL_URL}${
    import.meta.env.VITE_CONSOLE_PANEL_LOGIN_PATH
  }`
  return (
    <Stack className="align-items-center">
      <p>Please Login to Proceed</p>
      <a href={loginLink} target="_blank" rel="noopener noreferrer" className="w-100">
        <Button className="w-100">Login</Button>
      </a>
    </Stack>
  )
}

export default LoginPrompt
