import { siteConfig } from "$lib/config/site";

export const load = () => {
  return {
    meta: {
      title: siteConfig.meta.title,
      description: siteConfig.meta.description,
    }
  };
};