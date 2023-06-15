import React from 'react'
import Stack from 'react-bootstrap/Stack'

const LogoHeader = () => {
  return (
    <>
      <Stack direction="horizontal" gap={3} className="align-items-center">
        <img
          src="/img/logo-128.png"
          alt="logo"
          style={{
            width: '2rem',
          }}
        />
        <p
          style={{
            fontSize: '1.4rem',
            fontWeight: 'bold',
          }}
          className="text-logo m-0"
        >
          Trapper Client
        </p>
      </Stack>
    </>
  )
}

export default LogoHeader
