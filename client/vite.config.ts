import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    allowedHosts: [
      'ki-psychologie.student.vm.pve.fa1.hs-furtwangen.de',
      '141.28.73.25',
      'localhost'
    ]
  }
})
