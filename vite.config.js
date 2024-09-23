//vite.config.js
import { defineConfig } from 'vite'
import { djangoVitePlugin } from 'django-vite-plugin'

export default defineConfig({
    plugins: [
        djangoVitePlugin([
            'jsvite/js/main.js',
            // 'templatevite/css/style.css',
        ])
    ],
});