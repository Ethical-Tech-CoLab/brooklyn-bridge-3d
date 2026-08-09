import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// The viewer reads everything it needs from /public at runtime, so the same build serves any
// source-governed GLB by swapping model.config.json. Document-relative URLs are used throughout so
// that one build works both standalone and co-served under a district site root.
export default defineConfig({
  base: './',
  plugins: [react()],
  server: { port: 5174, strictPort: true },
  build: { outDir: 'dist', emptyOutDir: true },
});
