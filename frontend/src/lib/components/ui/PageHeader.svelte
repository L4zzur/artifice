<script lang="ts">
  import { ArrowLeft } from "lucide-svelte";
  import type { Snippet } from "svelte";

  interface Props {
    title: string;
    description: string;
    icon: Snippet;
    backLink?: {
      href: string;
      label: string;
    };
  }

  let { title, description, icon, backLink }: Props = $props();
</script>

<header class="page-header">
  {#if backLink}
    <a href={backLink.href} class="back-button">
      <ArrowLeft size={16} strokeWidth={2} />
      {backLink.label}
    </a>
  {/if}

  <div class="header-content">
    <div class="header-icon">
      {@render icon()}
    </div>
    <div class="header-title">
      <h1>{title}</h1>
      <p>{description}</p>
    </div>
  </div>
</header>

<style>
  .page-header {
    margin-bottom: 2rem;
  }

  .back-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.625rem 1.25rem;
    margin-bottom: 1rem;
    color: var(--md-sys-color-on-surface-variant);
    text-decoration: none;
    font-size: 0.95rem;
    font-weight: 500;
    border-radius: var(--md-sys-shape-corner-medium);
    transition: all var(--md-sys-animation-standard);
    background: var(--md-sys-color-surface-container);
    border: 1px solid var(--md-sys-color-outline-variant);
  }

  .back-button:hover {
    background: var(--md-sys-color-surface-container-high);
    color: var(--md-sys-color-primary);
    border-color: var(--md-sys-color-primary);
    transform: translateX(-4px);
  }

  .back-button:active {
    transform: translateX(-2px);
  }
  .header-content {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .header-icon {
    padding: 0.75rem;
    background: var(--md-sys-color-surface-container-high);
    border-radius: var(--md-sys-shape-corner-medium);
    color: var(--md-sys-color-primary);
  }

  h1 {
    font-size: 1.75rem;
    font-weight: 600;
    margin: 0 0 0.25rem 0;
    color: var(--md-sys-color-on-surface);
  }

  .header-content p {
    margin: 0;
    color: var(--md-sys-color-on-surface-variant);
  }
</style>
