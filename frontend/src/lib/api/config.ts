import { client } from './generated/client.gen';
import { PUBLIC_API_URL } from '$env/static/public';

client.setConfig({
  baseUrl: PUBLIC_API_URL || 'http://localhost:8000', 
});

export { client };
