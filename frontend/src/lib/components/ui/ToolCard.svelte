<script lang="ts">
  interface Props {
    icon: any;
    iconSize?: number;
    title: string;
    description: string;
    href: string;
    comingSoon?: boolean;
    variant?: "default" | "compact";
  }

  let {
    icon: Icon,
    iconSize,
    title,
    description,
    href,
    comingSoon,
    variant = "default",
  }: Props = $props();

  const size = iconSize || (variant === "compact" ? 32 : 48);
  const iconBoxSize = variant === "compact" ? 64 : 80;
</script>

{#if comingSoon}
  <div
    class="tool-card"
    class:compact={variant === "compact"}
    class:disabled={true}
  >
    <div
      class="tool-icon"
      style="width: {iconBoxSize}px; height: {iconBoxSize}px;"
    >
      <Icon {size} strokeWidth={1.5} />
    </div>
    <h3>{title}</h3>
    <p>{description}</p>
    <span class="coming-soon-badge">Coming Soon</span>
  </div>
{:else}
  <a {href} class="tool-card" class:compact={variant === "compact"}>
    <div
      class="tool-icon"
      style="width: {iconBoxSize}px; height: {iconBoxSize}px;"
    >
      <Icon {size} strokeWidth={1.5} />
    </div>
    <h3>{title}</h3>
    <p>{description}</p>
  </a>
{/if}

<style>
  .tool-card {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 2.5rem;
    background: var(--md-sys-color-surface-container);
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-large);
    text-decoration: none;
    color: inherit;
    transition: all var(--md-sys-animation-standard);
  }

  .tool-card.compact {
    padding: 2rem;
    box-shadow: none;
  }

  a.tool-card:hover {
    background: var(--md-sys-color-surface-container-high);
    border-color: var(--md-sys-color-primary);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  }

  a.tool-card:hover {
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
  }

  a.tool-card.compact:hover {
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  }

  .tool-card.disabled {
    opacity: 0.6;
    cursor: not-allowed;
    pointer-events: none;
  }

  .tool-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 80px;
    height: 80px;
    background: rgba(176, 196, 222, 0.15);
    border-radius: var(--md-sys-shape-corner-large);
    color: var(--md-sys-color-primary);
  }

  .tool-card.compact .tool-icon {
    border-radius: var(--md-sys-shape-corner-medium);
  }

  h3 {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--md-sys-color-on-surface);
    margin: 0;
  }

  .tool-card.compact h3 {
    font-size: 1.25rem;
  }

  p {
    color: var(--md-sys-color-on-surface-variant);
    line-height: 1.6;
    margin: 0;
  }

  .tool-card.compact p {
    line-height: 1.5;
  }

  .coming-soon-badge {
    position: absolute;
    top: 1rem;
    right: 1rem;
    padding: 0.375rem 0.875rem;
    background: var(--md-sys-color-tertiary-container);
    color: var(--md-sys-color-on-tertiary-container);
    border-radius: var(--md-sys-shape-corner-full);
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
</style>
