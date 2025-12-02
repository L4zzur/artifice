<script lang="ts">
  import ToolCard from "$lib/components/ui/ToolCard.svelte";
  import {
    KeyRound,
    CircleCheckBig,
    Sparkles,
    Fingerprint,
  } from "lucide-svelte";

  const tools = [
    {
      icon: Sparkles,
      title: "Hash Generator",
      description: "Generate cryptographic hashes with HMAC support",
      href: "/hash/generate",
      comingSoon: false,
    },
    {
      icon: CircleCheckBig,
      title: "Hash Verifier",
      description: "Verify data integrity with hash comparison",
      href: "/hash/verify",
      comingSoon: false,
    },
  ];
</script>

<div class="page-container">
  <header class="page-header">
    <div class="header-icon">
      <Fingerprint size={48} strokeWidth={1.7} />
    </div>
    <div class="header-title">
      <h1>Hash</h1>
      <p>Generate and verify cryptographic hashes for data integrity</p>
    </div>
  </header>

  <div class="tools-grid">
    {#each tools as tool}
      <ToolCard
        icon={tool.icon}
        title={tool.title}
        description={tool.description}
        href={tool.href}
        variant="compact"
        comingSoon={tool.comingSoon}
      />
    {/each}
  </div>
</div>

<style>
  .page-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
  }

  .page-header {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    margin-bottom: 3rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid var(--md-sys-color-outline-variant);
  }

  .header-icon {
    padding: 1rem;
    background: var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-large);
    color: var(--md-sys-color-primary);
  }

  h1 {
    font-size: 2rem;
    font-weight: 600;
    color: var(--md-sys-color-on-surface);
    margin: 0 0 0.5rem 0;
  }

  .page-header p {
    color: var(--md-sys-color-on-surface-variant);
    margin: 0;
  }

  .tools-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
  }
</style>
