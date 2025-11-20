import { Github, Globe, Send } from "lucide-svelte";

export const siteConfig = {
  name: "Artifice",
  description: "A collection of powerful web tools for developers and creators",
  url: "https://artifice-toolkit.dev",

  links: [
    {
      name: "GitHub",
      href: "https://github.com/L4zzur/artifice",
      icon: Github,
    },
    {
      name: "Telegram",
      href: "https://t.me/L4zzq_blog",
      icon: Send,
    },
    {
      name: "Author",
      href: "https://l4zzur.top",
      icon: Globe,
    },
  ],

  meta: {
    title: "Artifice - Powerful Web Toolkit",
    description:
      "A collection of powerful web tools including QR code generator, password manager, and more.",
    keywords: ["qr code", "password generator", "web tools", "developer tools"],
  },
};

export type SiteConfig = typeof siteConfig;
