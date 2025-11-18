import { defineConfig } from '@hey-api/openapi-ts';

export default defineConfig({
  client: '@hey-api/client-fetch',
  input: './openapi.json', 
  output: {
    path: './src/lib/api/generated', 
    format: 'prettier', 
    lint: 'eslint',
  },
  plugins: ['@hey-api/client-fetch'],
  types: {
    enums: 'typescript',
  },
  services: {
    asClass: false,
  },
});
