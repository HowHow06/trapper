import React from 'react'
import { Button, Stack } from 'react-bootstrap'

const LoginPrompt = () => {
  return (
    <Stack className="align-items-center">
      <p>Please Login to Proceed</p>
      <a
        href="https://localhost:3000/auth/login"
        target="_blank"
        rel="noopener noreferrer"
        className="w-100"
      >
        <Button className="w-100">Login</Button>
      </a>
    </Stack>
  )
}

export default LoginPrompt
