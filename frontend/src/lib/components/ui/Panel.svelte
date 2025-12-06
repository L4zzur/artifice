<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    title?: string;
    padding?: "default" | "large" | "small";
    height?: string;
    header?: Snippet;
    children: Snippet;
  }

  let { title, padding = "small", height, header, children }: Props = $props();

  const paddingMap = {
    small: "1.5rem",
    default: "2rem",
    large: "2.5rem",
  };
</script>

<section
  class="panel"
  style="padding: {paddingMap[padding]}
  {height ? `; height: ${height}` : ''}"
>
  {#if header}
    <div class="panel-header">
      {@render header()}
    </div>
  {:else if title}
    <h2 class="panel-title">{title}</h2>
  {/if}

  <div class="panel-content">
    {@render children()}
  </div>
</section>

<style>
  .panel {
    background: var(--md-sys-color-surface-container);
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-large);
    display: flex;
    flex-direction: column;
  }

  .panel-header {
    margin-bottom: 0.5rem;
    flex-shrink: 0;
  }

  .panel-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0 0 0.75rem 0;
    color: var(--md-sys-color-on-surface);
    flex-shrink: 0;
  }

  .panel-content {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    flex: 1;
    min-height: 0;
  }
</style>
