import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import './index.css'

const rootElement = document.getElementById('root')
if (rootElement) {
  rootElement.style.width = '100%'
  rootElement.style.height = '100%'
}

createRoot(rootElement!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)