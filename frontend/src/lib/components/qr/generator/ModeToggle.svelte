<script lang="ts">
  import { Sparkles } from "lucide-svelte";

  interface Props {
    useStyledImage: boolean;
    onToggle: (advanced: boolean) => void;
  }

  let { useStyledImage, onToggle }: Props = $props();
</script>

<div class="mode-toggle">
  <button
    class="mode-button"
    class:active={!useStyledImage}
    onclick={() => {
      onToggle(false);
    }}
  >
    Basic
  </button>

  <button
    class="mode-button"
    class:active={useStyledImage}
    onclick={() => {
      onToggle(true);
    }}
  >
    <Sparkles size={16} />
    Advanced
  </button>
</div>

<style>
  .mode-toggle {
    display: flex;
    gap: 0.5rem;
    padding: 0.25rem;
    background: var(--md-sys-color-surface-container-high);
    border-radius: var(--md-sys-shape-corner-medium);
  }

  .mode-button {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.625rem;
    background: transparent;
    border: none;
    border-radius: var(--md-sys-shape-corner-small);
    color: var(--md-sys-color-on-surface-variant);
    font-weight: 500;
    cursor: pointer;
    transition: all var(--md-sys-animation-standard);
  }

  .mode-button:hover {
    background: var(--md-sys-color-surface-container);
  }

  .mode-button.active {
    background: var(--md-sys-color-primary);
    color: var(--md-sys-color-on-primary);
  }
</style>
