import React from 'react'
import { Button } from 'react-bootstrap'

const BaseActionButton = ({ className, icon, text, ...rest }) => {
  return (
    <Button className={`hstack gap-2 justify-content-center ${className}`} {...rest}>
      <span className="icon-btn">{icon}</span>
      <span>{text}</span>
    </Button>
  )
}

export default BaseActionButton
