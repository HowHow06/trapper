import React from 'react'
import LogoHeader from './LogoHeader'

const PopupContainer = ({ children }) => {
  return (
    <div
      style={{
        width: '20rem',
      }}
      className="bg-white py-3 px-4"
    >
      <LogoHeader />
      <hr />
      {children}
    </div>
  )
}

export default PopupContainer
