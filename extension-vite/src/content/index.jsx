import React from 'react'
import ReactDOM from 'react-dom/client'

const appContainer = document.createElement('div')
if (!appContainer) {
  throw new Error('Cannot find container')
}

document.body.appendChild(appContainer)
ReactDOM.createRoot(appContainer).render(
  <React.StrictMode>
    <div>Hello Im ContentScipt DOM</div>
  </React.StrictMode>,
)

// cannot import component from other file, else will show error Error: @vitejs/plugin-react can't detect preamble. Something is wrong. See https://github.com/vitejs/vite-plugin-react/pull/11#discussion_r430879201
// if want to use this jsx file, change in manifest.js
