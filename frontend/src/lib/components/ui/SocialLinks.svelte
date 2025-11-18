<script lang="ts">
  import { siteConfig } from "$lib/config/site";

  interface Props {
    variant?: "default" | "compact";
  }

  let { variant = "default" }: Props = $props();
</script>

<div class="social-links" class:compact={variant === "compact"}>
  {#each siteConfig.links as link}
    <a
      href={link.href}
      target="_blank"
      rel="noopener noreferrer"
      class="social-link"
      aria-label={link.name}
      title={link.name}
    >
      <link.icon size={20} strokeWidth={1.5} />
    </a>
  {/each}
</div>

<style>
  .social-links {
    display: flex;
    gap: 0.75rem;
    align-items: center;
  }

  .social-link {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    background: var(--md-sys-color-surface-container);
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-medium);
    color: var(--md-sys-color-on-surface-variant);
    text-decoration: none;
    transition: all var(--md-sys-animation-standard);
  }

  .social-link:hover {
    background: var(--md-sys-color-surface-container-high);
    color: var(--md-sys-color-primary);
    border-color: var(--md-sys-color-primary);
    transform: translateY(-2px);
  }

  .social-link:active {
    transform: translateY(0);
  }

  .social-links.compact .social-link {
    width: 36px;
    height: 36px;
  }
</style>
