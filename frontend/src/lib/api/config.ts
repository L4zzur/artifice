import { client } from './generated/client.gen';
import { API_URL } from '$env/static/public';

client.setConfig({
  baseUrl: API_URL || 'http://localhost:8000', 
});

export { client };
