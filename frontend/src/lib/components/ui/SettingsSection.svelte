<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    h3: string;
    icon?: any;
    iconSize?: number;
    iconStrokeWidth?: number;
    children: Snippet;
  }

  let {
    h3,
    icon: Icon,
    iconSize = 18,
    iconStrokeWidth = 2,
    children,
  }: Props = $props();
</script>

<div class="settings-section">
  <h3>
    {#if Icon}
      <Icon size={iconSize} />
    {/if}
    {h3}
  </h3>
  {@render children()}
</div>

<style>
  .settings-section {
    margin: 0.75rem 0 0 0;
    padding: 0.75rem 0 0 0;
    border-top: 1px solid var(--md-sys-color-outline-variant);
  }

  .settings-section h3 {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1rem;
    font-weight: 600;
    margin: 0 0 1rem 0;
    color: var(--md-sys-color-on-surface);
  }
</style>
