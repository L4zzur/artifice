<script lang="ts">
  import Button from "$lib/components/ui/Button.svelte";
  import Panel from "$lib/components/ui/Panel.svelte";
  import { Copy } from "lucide-svelte";

  interface Props {
    hash: string | null;
    onCopy: () => void;
  }

  let { hash, onCopy }: Props = $props();
</script>

<Panel title="Generated Hash">
  {#if hash}
    <div class="hash-display">
      <div class="hash-value">
        <code>{hash}</code>
      </div>
      <div class="hash-actions">
        <Button onclick={onCopy} fullWidth>
          <Copy size={16} />Copy
        </Button>
      </div>
    </div>
  {:else}
    <div class="placeholder">
      <p>Your generated hash will appear here</p>
    </div>
  {/if}
</Panel>

<style>
  .hash-display {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .hash-value {
    padding: 1.5rem;
    background: var(--md-sys-color-surface-container-high);
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-medium);
    font-family: "Courier New", Consolas, Monaco, monospace;
    font-size: 0.9375rem;
    word-break: break-all;
    color: var(--md-sys-color-on-surface);
    line-height: 1.6;
  }

  .hash-actions {
    display: flex;
    gap: 0.75rem;
  }

  .placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 1rem;
    text-align: center;
  }

  .placeholder p {
    margin: 0;
    color: var(--md-sys-color-on-surface-variant);
    font-size: 0.9375rem;
  }
</style>
