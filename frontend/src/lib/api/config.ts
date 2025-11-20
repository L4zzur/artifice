import { client } from "./generated/client.gen";
import { env } from "$env/dynamic/public";

client.setConfig({
  baseUrl: env.PUBLIC_API_URL,
});

export { client };
