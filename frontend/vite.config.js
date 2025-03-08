import { fileURLToPath, URL } from 'node:url'
import legacy from '@vitejs/plugin-legacy'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'

// https://vitejs.dev/config/
export default defineConfig({
  base: './',
  plugins: [
    vue({
      template: {
        compilerOptions: {
          isCustomElement: (tag) => ['vue-advanced-chat', 'emoji-picker'].includes(tag),
        },
      },
    }),
    AutoImport({
      // Specify imports to auto-import
      imports: [
        'vue',
        'vue-router',
        // You can add more frameworks here if needed
      ],
      dts: './auto-imports.d.ts', // Generate TypeScript declaration
      eslintrc: {
        enabled: true, // Generate ESLint configuration
      },
    }),
    Components({
      // Allow auto import and registration of components
      dirs: ['src/components'],
      extensions: ['vue'],
      dts: true,
    }),
  ],

  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
