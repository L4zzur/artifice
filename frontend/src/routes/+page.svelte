<script lang="ts">
  import {
    Fingerprint,
    KeyRound,
    MegaphoneOff,
    QrCode,
    SquareCode,
    Zap,
  } from "lucide-svelte";

  import icon from "$lib/assets/icon.png";

  import ToolCard from "$lib/components/ui/ToolCard.svelte";
  import SocialLinks from "$lib/components/ui/SocialLinks.svelte";

  const tools = [
    {
      icon: QrCode,
      title: "QR Code Tools",
      description: "Generate and scan QR codes with ease",
      href: "/qr",
      comingSoon: false,
    },
    {
      icon: KeyRound,
      title: "Password Tools",
      description: "Generate strong and secure passwords",
      href: "/password",
      comingSoon: false,
    },
    {
      icon: Fingerprint,
      title: "Hash Tools",
      description: "Generate and verify cryptographic hashes",
      href: "/hash",
      comingSoon: false,
    },
    {
      icon: Zap,
      title: "More Tools",
      description: "Additional utilities coming soon",
      href: "#",
      comingSoon: true,
    },
  ];
</script>

<div class="page-container">
  <div class="page-header">
    <SocialLinks />
  </div>

  <section class="hero">
    <div class="hero-content">
      <div class="hero-icon">
        <img src={icon} alt="Artifice Toolkit" />
      </div>
      <h1>Artifice Toolkit</h1>
      <p class="hero-subtitle">
        A collection of powerful web tools for developers and creators
      </p>
      <div class="hero-features">
        <span class="hero-feature-badge">
          <SquareCode size={16} strokeWidth={2} />
          Open Source
        </span>
        <span class="hero-feature-badge">
          <MegaphoneOff size={16} strokeWidth={2} />
          No Ads or Tracking
        </span>
        <span class="hero-feature-badge">
          <Zap size={16} strokeWidth={2} />
          Fast & Simple
        </span>
      </div>
    </div>
  </section>

  <section class="tools">
    <h2>Available Tools</h2>
    <div class="tools-grid">
      {#each tools as tool}
        <ToolCard
          icon={tool.icon}
          title={tool.title}
          description={tool.description}
          href={tool.href}
          comingSoon={tool.comingSoon}
        />
      {/each}
    </div>
  </section>
</div>

<style>
  .page-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    padding: 1rem;
    max-width: 1400px;
    margin: 0 auto;
  }

  .page-header {
    display: flex;
    justify-content: flex-end;
    padding: 1rem 0 0 0;
  }

  .hero {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 25rem;
    text-align: center;
  }

  .hero-content {
    max-width: 800px;
  }

  .hero-icon {
    display: inline-flex;
    padding: 1.5rem;
    background: var(--md-sys-color-primary-container);
    border-radius: var(--md-sys-shape-corner-extra-large);
    color: var(--md-sys-color-primary);
    margin-bottom: 2rem;
  }

  .hero-icon img {
    width: 80px;
    height: 80px;
    object-fit: contain;
    filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.308));
  }

  h1 {
    font-size: 3.5rem;
    font-weight: 700;
    color: var(--md-sys-color-on-surface);
    margin: 0 0 1rem 0;
    background: linear-gradient(
      135deg,
      var(--md-sys-color-primary),
      var(--md-sys-color-tertiary)
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .hero-subtitle {
    font-size: 1.25rem;
    color: var(--md-sys-color-on-surface-variant);
    margin: 0 0 2rem 0;
    line-height: 1.6;
  }

  .hero-features {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
  }

  .hero-feature-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.625rem 1.25rem;
    background: var(--md-sys-color-surface-container-high);
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-full);
    color: var(--md-sys-color-on-surface);
    font-weight: 500;
    font-size: 0.95rem;
  }

  .tools h2 {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 600;
    color: var(--md-sys-color-on-surface);
    margin: 0 0 3rem 0;
  }

  .tools-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem;
  }

  @media (max-width: 768px) {
    h1 {
      font-size: 2.5rem;
    }

    .hero-subtitle {
      font-size: 1.125rem;
    }

    .tools h2 {
      font-size: 2rem;
    }

    .tools-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
